'''
Module contains testing class
'''

from biography import Biography
from training import Training

class Testing:
    '''
    Classifies a list of biographies using probabilities calculated during training
    Properties:
    testing_set - the list of biographies to be classified
    size - the number of biographies to be classified
    training - the training set used to classify biographies
    '''
    def __init__(self, testing_set: list[Biography], training: Training) -> None:
        self.testing_set = testing_set
        self.size = len(self.testing_set)
        self.training = training

    def compute_category_logs(self, biography: Biography) -> dict[str, float]:
        '''
        Given a biography, computes the negative log of the probability
            the biography is in any given category in the categories
            from training
        '''
        biography_logs = {}
        for category in self.training.categories:
            log = self.training.category_logs[category]
            for word in biography.words:
                if word in self.training.words:
                    log += self.training.word_category_logs[category][word]
                else:
                    log += self.training.default_word_category_log
            biography_logs[category] = log
        return biography_logs

    def compute_category_probs(self, biography: Biography) -> dict[str, float]:
        '''
        Given a biography, computes the probability the biography is in any
            given category by recovering probabilities from the negative logs
        '''
        biography_logs = self.compute_category_logs(biography)
        m = min(biography_logs.values())
        s = 0
        probs = {}
        for (category, log) in biography_logs.items():
            if log - m < 7:
                xi = 2 ** (m - log)
            else:
                xi = 0
            s += xi
            probs[category] = xi

        for category in probs:
            probs[category] /= s

        return probs

    def display_biography_prediction(self, biography: Biography) -> bool:
        '''
        Given a biography, computes the probability the biography is of
            any given category, and reports the probabilities, the highest
            probability category, and if the categorization was correct
        '''
        category_probs = self.compute_category_probs(biography)
        max_prob = 0
        for (category, prob) in category_probs.items():
            if prob > max_prob:
                prediction = category
                max_prob = prob
        print(f'{biography.name}.', end='   ')
        print(f'Prediction: {prediction.capitalize()}.', end='   ')
        is_correct = prediction == biography.category
        print("Right." if is_correct else "Wrong.")
        for (category, prob) in category_probs.items():
            print(f'{category.capitalize()}: {prob:.2f}', end='   ')
        print('\n')
        return is_correct

    def print_results(self) -> None:
        '''
        Displays predictions for all biographies in the testing set and reports
            the accuracy of the classifier on the testing set
        '''
        correct = 0
        for biography in self.testing_set:
            if self.display_biography_prediction(biography):
                correct += 1
        print(f'Overall accuracy: {correct} out of {self.size} = {correct/self.size:.2f}')
