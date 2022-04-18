import math
from biography import Biography
from training import Training

class Testing:
    def __init__(self, file_name: str, N: int, training: Training, testing_set: list[Biography] = []) -> None:
        with open(file_name, 'r') as file:
            self.testing_set = [Biography(s.strip()) for s in file.read().split('\n\n') if s.strip() != ''][N:]
        # self.testing_set = testing_set
        self.size = len(self.testing_set)
        self.training = training
    
    def compute_category_logs(self, biography: Biography) -> dict[str, float]:
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
        
        for category in probs.keys():
            probs[category] /= s
        
        return probs
    
    def display_biography_prediction(self, biography: Biography) -> bool:
        category_probs = self.compute_category_probs(biography)
        max_prob = 0
        for (category, prob) in category_probs.items():
            if prob > max_prob:
                prediction = category
                max_prob = prob
        print(f'{biography.name}.', end='   ')
        print(f'Prediction: {prediction.capitalize()}.', end='   ')
        if prediction == biography.category:
            is_correct = True
        else:
            is_correct = False
        print("Right." if is_correct else "Wrong.")
        for (category, prob) in category_probs.items():
            print(f'{category.capitalize()}: {prob:.2f}', end='   ')
        print('\n')
        return is_correct

    def print_results(self) -> None:
        correct = 0
        for biography in self.testing_set:
            if self.display_biography_prediction(biography):
                correct += 1
        print(f'Overall accuracy: {correct} out of {self.size} = {correct/self.size:.2f}')

if __name__ == "__main__":
    training = Training('tinyCorpus.txt', 5)
    training.train()
    testing = Testing('tinyCorpus.txt', 5, training)
    testing.print_results()
