## Relation-Networks-Keras-Implementation

### Introduction
This is a Keras Implementation of the paper "[A simple neural network module for relational reasoning](https://nurture.ai/p/089570b9-fe63-43af-8a25-76117d2a1c21)" as part of the [NIPS Global Paper Implementation Challenge](https://nurture.ai/nips-challenge)

### Results

#### Model with Relation Network (CNN + RN) at 20th Epoch

|               | Accuracy      |
| ------------- | ------------- |
| Relational    | 0.847917  |
| Non-Relational | 0.961458 |
| Overall       | 0.903125|

#### Baseline Model (CNN + MLP) at 100th Epoch

|               | Accuracy      |
| ------------- | ------------- |
| Relational    | 0.796875  |
| Non-Relational | 0.908854 |
| Overall       | 0.828385|


It can be seen that, even at lower number of training epoch, the CNN+RN model produced better results in both Relational and Non-Relational questions. This fits the result presented with the paper. However, my Baseline Model Relational Question accuracy is much higher than the Baseline Model accuracy stated by the paper (%63). I think this difference is caused by the authors using a model too complex for the problem. In my baseline model, I have used much lower number of hidden units in my networks as compared to the authors' networks. (This was mainly due to my computer's memory constraints). However, my baseline model performed much better than the author's baseline model, demonstrating that the author's baseline model had overfitted to their training data. This demonstrated that, while the author's claim that CNN+RN performs much than CNN+MLP in relational question tasks is true, the difference is not as large as the one reported in the paper.
