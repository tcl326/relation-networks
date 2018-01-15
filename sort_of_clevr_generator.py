import numpy as np
from math import radians, cos
import cv2

class SortOfCLEVRGenerator(object):
    colors = [
        (0,0,255),      #red
        (255,0,0),      #blue
        (0,255,0),      #green
        (0,156,255),    #orange
        (0,255,255),    #yellow
        (128,128,128)   #grey
    ]
    shapes = [
        's',    #square
        'c',    #circle
    ]

    img_size = 128
    shape_size = 25

    question_vector_size = 11
    answer_vector_size = 10

    def __init__(self, number_questions=10, number_shapes=6):
        self.number_questions = number_questions
        self.number_shapes = number_shapes

    def generate_centers(self):
        centers = []
        for n in xrange(self.number_shapes):
            collision = True
            while collision:
                center = np.random.randint(self.shape_size, self.img_size - self.shape_size, 2)
                collision = False
                for c in centers:
                    if ((center-c)**2).sum() < (self.shape_size)**2:
                        collision = True
            centers.append(center)
        return centers

    def generate_sample(self):
        centers = self.generate_centers()
        shape_choice = np.random.randint(2, size=self.number_shapes)
        img = np.zeros((self.img_size,self.img_size,3))
        representation = []
        for idx, c in enumerate(centers):
            shape = self.shapes[shape_choice[idx]]
            if shape == 's':
                const = int(self.shape_size * cos(radians(45))/2)
                start = (c[0]-const, c[1]-const)
                end = (c[0]+const, c[1]+const)
                img = cv2.rectangle(img, start, end, self.colors[idx], -1)
            else:
                img = cv2.circle(img, (c[0], c[1]), self.shape_size/2, self.colors[idx], -1)
            representation.append([c, shape])
        return img, representation

    def generate_questions(self, representation, number_questions=10):
        # [red, blue, green, orange, yellow, gray, relational, non-relational, question 1, question 2, question 3]
        questions = []
        for q in xrange(number_questions):
            for r in xrange(2):
                question = [0] * self.question_vector_size
                color = np.random.randint(6)
                question[color] = 1
                question[6 + r] = 1
                question_type = np.random.randint(3)
                question[8 + question_type] = 1
                questions.append(question)
        return questions

    def generate_answers(self, representation, questions):
        #[yes, no, square, circle, 1, 2, 3, 4, 5, 6]
        answers = []
        for question in questions:
            answer = [0] * self.answer_vector_size
            color = question[:6].index(1)
            if question[6]:
                if question[8]: #The shape of the nearest object?
                    dist = [((representation[color][0]-obj[0])**2).sum() for obj in representation]
                    dist[dist.index(0)] = float('inf')
                    closest = dist.index(min(dist))
                    if representation[closest][1] == 's':
                        answer[2] = 1
                    else:
                        answer[3] = 1
                elif question[9]: #The shape of the farthest object?
                    dist = [((representation[color][0]-obj[0])**2).sum() for obj in representation]
                    furthest = dist.index(max(dist))
                    if representation[furthest][1] == 's':
                        answer[2] = 1
                    else:
                        answer[3] = 1

                else: #How many objects have the same shape?
                    count = -1
                    shape = representation[color][1]
                    for obj in representation:
                        if obj[1] == shape:
                            count += 1
                    answer[count + 4] = 1
            else:
                if question[8]: #Is it a circle or a rectangle?
                    if representation[color][1] == 's':
                        answer[2] = 1
                    else:
                        answer[3] = 1
                elif question[9]: #Is it on the bottom of the image?
                    if representation[color][0][1] > self.img_size/2:
                        answer[0] = 1
                    else:
                        answer[1] = 1
                else: #Is it on the left of the image?
                    if representation[color][0][0] > self.img_size/2:
                        answer[1] = 1
                    else:
                        answer[0] = 1
            answers.append(answer)
        return answers

    def generate_dataset(self):
        img, representation = self.generate_sample()
        questions = self.generate_questions(representation)
        answers = self.generate_answers(representation, questions)
        dataset = (img, questions, answers)
        return dataset

# import cv2
# import os
# import numpy as np
# import pickle
#
# train_size = 9800
# test_size = 200
# img_size = 128
# size = 5
# question_size = 11 ##6 for one-hot vector of color, 2 for question type, 3 for question subtype
# """Answer : [yes, no, rectangle, circle, r, g, b, o, k, y]"""
#
# nb_questions = 10
# dirs = './data'
#
# colors = [
#     (0,0,255),##r
#     (0,255,0),##g
#     (255,0,0),##b
#     (0,156,255),##o
#     (128,128,128),##k
#     (0,255,255)##y
# ]
#
#
# try:
#     os.makedirs(dirs)
# except:
#     print('directory {} already exists'.format(dirs))
#
# def center_generate(objects):
#     while True:
#         pas = True
#         center = np.random.randint(0+size, img_size - size, 2)
#         if len(objects) > 0:
#             for name,c,shape in objects:
#                 if ((center - c) ** 2).sum() < ((size * 2) ** 2):
#                     pas = False
#         if pas:
#             return center
#
#
#
# def build_dataset():
#     objects = []
#     img = np.ones((img_size,img_size,3)) * 255
#     for color_id,color in enumerate(colors):
#         center = center_generate(objects)
#         if random.random()<0.5:
#             start = (center[0]-size, center[1]-size)
#             end = (center[0]+size, center[1]+size)
#             cv2.rectangle(img, start, end, color, -1)
#             objects.append((color_id,center,'r'))
#         else:
#             center_ = (center[0], center[1])
#             cv2.circle(img, center_, size, color, -1)
#             objects.append((color_id,center,'c'))
#
#
#     rel_questions = []
#     norel_questions = []
#     rel_answers = []
#     norel_answers = []
#     """Non-relational questions"""
#     for _ in range(nb_questions):
#         question = np.zeros((question_size))
#         color = random.randint(0,5)
#         question[color] = 1
#         question[6] = 1
#         subtype = random.randint(0,2)
#         question[subtype+8] = 1
#         norel_questions.append(question)
#         """Answer : [yes, no, rectangle, circle, r, g, b, o, k, y]"""
#         if subtype == 0:
#             """query shape->rectangle/circle"""
#             if objects[color][2] == 'r':
#                 answer = 2
#             else:
#                 answer = 3
#
#         elif subtype == 1:
#             """query horizontal position->yes/no"""
#             if objects[color][1][0] < img_size / 2:
#                 answer = 0
#             else:
#                 answer = 1
#
#         elif subtype == 2:
#             """query vertical position->yes/no"""
#             if objects[color][1][1] < img_size / 2:
#                 answer = 0
#             else:
#                 answer = 1
#         norel_answers.append(answer)
#
#     """Relational questions"""
#     for i in range(nb_questions):
#         question = np.zeros((question_size))
#         color = random.randint(0,5)
#         question[color] = 1
#         question[7] = 1
#         subtype = random.randint(0,2)
#         question[subtype+8] = 1
#         rel_questions.append(question)
#
#         if subtype == 0:
#             """closest-to->rectangle/circle"""
#             my_obj = objects[color][1]
#             dist_list = [((my_obj - obj[1]) ** 2).sum() for obj in objects]
#             dist_list[dist_list.index(0)] = 999
#             closest = dist_list.index(min(dist_list))
#             if objects[closest][2] == 'r':
#                 answer = 2
#             else:
#                 answer = 3
#
#         elif subtype == 1:
#             """furthest-from->rectangle/circle"""
#             my_obj = objects[color][1]
#             dist_list = [((my_obj - obj[1]) ** 2).sum() for obj in objects]
#             furthest = dist_list.index(max(dist_list))
#             if objects[furthest][2] == 'r':
#                 answer = 2
#             else:
#                 answer = 3
#
#         elif subtype == 2:
#             """count->1~6"""
#             my_obj = objects[color][2]
#             count = -1
#             for obj in objects:
#                 if obj[2] == my_obj:
#                     count +=1
#             answer = count+4
#
#         rel_answers.append(answer)
#
#     relations = (rel_questions, rel_answers)
#     norelations = (norel_questions, norel_answers)
#
#     img = img/255.
#     dataset = (img, relations, norelations)
#     return dataset
#
#
# print('building test datasets...')
# test_datasets = [build_dataset() for _ in range(test_size)]
# print('building train datasets...')
# train_datasets = [build_dataset() for _ in range(train_size)]
#
#
# #img_count = 0
# #cv2.imwrite(os.path.join(dirs,'{}.png'.format(img_count)), cv2.resize(train_datasets[0][0]*255, (512,512)))
#
#
# print('saving datasets...')
# filename = os.path.join(dirs,'sort-of-clevr.pickle')
# with  open(filename, 'wb') as f:
#     pickle.dump((train_datasets, test_datasets), f)
# print('datasets saved at {}'.format(filename))
