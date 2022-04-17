import math
from biography import Biography

class Training:
    def __init__(self, file_name: str, N: int) -> None:
        with open(file_name, 'r') as file:
            self.training_set = [Biography(s.strip()) for s in file.read().split('\n\n') if s != ''][:N]

        words = []
        categories = []
        for biography in self.training_set:
            words += biography.words
            categories.append(biography.category)
        self.words = set(words)
        self.categories = set(categories)

        self.epsilon = 0.1
        self.size = N

    def compute_probabilities(self) -> None:
        # initialize
        self.category_probs = {category: 0 for category in self.categories}
        self.word_category_probs = {category: {word: 0 for word in self.words} for category in self.categories}

        # calculate occurances
        for biography in self.training_set:
            self.category_probs[biography.category] += 1
            for word in self.words:
                if word in biography.words:
                    self.word_category_probs[biography.category][word] += 1
        
        # calculate frequencies, their lapalacian corrections, and negative log
        for category in self.categories:
            occ_c = self.category_probs[category]
            for word in self.words:
                self.word_category_probs[category][word] = -math.log(self.laplacian_correction(self.word_category_probs[category][word]/occ_c, 2, self.epsilon), 2)
            self.category_probs[category] = -math.log(self.laplacian_correction(self.category_probs[category]/self.size, len(self.categories), self.epsilon), 2)
    
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