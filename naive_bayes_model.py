'''
Module contains the Naive_Bayes_Model class
'''

import sys
from biography import Biography
from training import Training
from testing import Testing

class NaiveBayesModel:
    '''
    Represents the entire Naive Bayes Model by training on N biographies from
        a file with the Naive Bayes method, and testing on the remaining biographies
    Properties:
    training_set - the set to train on. the first N biographies in the file
    testing_set - the set to test on. the remaining biographies in the file
    training - the training model. not computed until self.train is called
    '''
    def __init__(self, file_name: str, N: int) -> None:
        with open(file_name, 'r', encoding="utf-8") as file:
            self.biographies = [Biography(s.strip())\
                for s in file.read().split('\n\n') if s.strip() != '']
        self.training_set = self.biographies[:N]
        self.testing_set = self.biographies[N:]
        self.training = None

    def train(self) -> None:
        '''
        Trains the model out of the training set.
        '''
        self.training = Training(self.training_set)
        self.training.train()

    def run_inference(self) -> None:
        '''
        Runs predictions on the testing set
        '''
        if self.training is None:
            print("Please train the model first.")
        else:
            testing = Testing(self.testing_set, self.training)
            testing.print_results()

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Incorrect number of input arguments. Try again.")
        sys.exit(1)
    nb = NaiveBayesModel(sys.argv[1], int(sys.argv[2]))
    nb.train()
    nb.run_inference()
    