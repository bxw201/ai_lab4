import math
from biography import Biography

class Training:
    def __init__(self, training_set: list[Biography]) -> None:
        self.training_set = training_set

        words = []
        categories = []
        for biography in self.training_set:
            words += biography.words
            categories.append(biography.category)
        self.words = set(words)
        self.categories = set(categories)

        self.epsilon = 0.1
        self.size = len(self.training_set)

    def train(self) -> None:
        # initialize
        self.category_logs = {category: 0 for category in self.categories}
        self.word_category_logs = {category: {word: 0 for word in self.words} for category in self.categories}

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
                self.word_category_logs[category][word] = -math.log(self.laplacian_correction(self.word_category_logs[category][word]/occ_c, 2, self.epsilon), 2)
            self.category_logs[category] = -math.log(self.laplacian_correction(self.category_logs[category]/self.size, len(self.categories), self.epsilon), 2)
        
        # use when the word in the testing set does not appear in the testing set
        self.default_word_category_log = -math.log(self.epsilon/(1 + 2 * self.epsilon), 2)
    
    @staticmethod
    def laplacian_correction(freq: int, categories: int, epsilon: float) -> float:
        return (freq + epsilon)/(1 + categories * epsilon)

    def display(self) -> None:
        for biography in self.training_set:
            biography.display()
        print(self.words)

if __name__ == "__main__":
    T = Training("bioCorpus.txt", 5)
    T.display()