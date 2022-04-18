import sys
from biography import Biography
from training import Training
from testing import Testing

class Naive_Bayes_Model:
    def __init__(self, file_name: str, N: int) -> None:
        with open(file_name, 'r') as file:
            self.biographies = [Biography(s.strip()) for s in file.read().split('\n\n') if s.strip() != '']
        self.training_set = self.biographies[:N]
        self.testing_set = self.biographies[N:]
        self.training = None

    def train(self) -> None:
        self.training = Training(self.training_set)
        self.training.train()
    
    def run_inference(self) -> None:
        if self.training == None:
            print("Please train the model first.")
        else:
            testing = Testing(self.testing_set, self.training)
            testing.print_results()

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Incorrect number of input arguments. Try again.")
        sys.exit(1)
    nb = Naive_Bayes_Model(sys.argv[1], int(sys.argv[2]))
    nb.train()
    nb.run_inference()
    