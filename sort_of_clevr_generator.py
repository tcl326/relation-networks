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

    img_size = 75
    shape_size = 10

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
        dataset = (img.astype('float32'), questions, answers)
        return dataset
