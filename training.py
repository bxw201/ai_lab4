from biography import Biography

class Training:
    def __init__(self, file_name: str, N: int) -> None:
        with open(file_name, 'r') as file:
            self.biographies = [Biography(s.strip()) for s in file.read().split('\n\n') if s != '']
    
    def display(self) -> None:
        for biography in self.biographies:
            biography.display()

if __name__ == "__main__":
    T = Training("bioCorpus.txt", 5)
    T.display()