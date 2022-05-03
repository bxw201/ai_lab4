'''
Module contains Training class
'''

import math
from biography import Biography

class Training:
    '''
    Performs training computations on a list of biographies
    Properties:
    training_set - the list of biographies to be trained on
    words - the set of all important words used in the biographies
    categories - the set of all categories in the biographies
    category_logs - dictionary associating a category v with -log(P(C=v))
    word_category_logs - dictionary associating a word w and a category v
                         with -log(P(w|C=v))
    default_word_category_log - the negative log to use in testing when the
                                word encountered has not been seen in the
                                training set
    epsilon - factor for laplacian correction
    size - the number of biographies in the training set
    '''
    def __init__(self, training_set: list[Biography]) -> None:
        self.training_set = training_set

        words = []
        categories = []
        for biography in self.training_set:
            words += biography.words
            categories.append(biography.category)
        self.words = set(words)
        self.categories = set(categories)

        # to be computed in self.train
        self.category_logs = None
        self.word_category_logs = None
        self.default_word_category_log = None

        self.epsilon = 0.1
        self.size = len(self.training_set)

    def train(self) -> None:
        '''
        Trains the model by computing self.category_logs and self.word_category_logs
        '''
        # initialize
        self.category_logs = {category: 0 for category in self.categories}
        self.word_category_logs = {category: {word: 0 for word in self.words} \
            for category in self.categories}

        # calculate occurances
        for biography in self.training_set:
            self.category_logs[biography.category] += 1
            for word in self.words:
                if word in biography.words:
                    self.word_category_logs[biography.category][word] += 1

        # calculate frequencies, their lapalacian corrections, and negative log
        for category in self.categories:
            occ_c = self.category_logs[category]
            for word in self.words:
                self.word_category_logs[category][word] = -math.log(self.laplacian_correction\
                    (self.word_category_logs[category][word]/occ_c, 2, self.epsilon), 2)
            self.category_logs[category] = -math.log(self.laplacian_correction\
                (self.category_logs[category]/self.size, len(self.categories), self.epsilon), 2)

        # use when the word in the testing set does not appear in the testing set
        self.default_word_category_log = -math.log(self.epsilon/(1 + 2 * self.epsilon), 2)

    @staticmethod
    def laplacian_correction(freq: int, categories: int, epsilon: float) -> float:
        '''
        Returns the probability computed using the Laplacian correction
        '''
        return (freq + epsilon)/(1 + categories * epsilon)

    def display(self) -> None:
        '''
        Prints class to the console
        '''
        for biography in self.training_set:
            biography.display()
        print(self.words)
