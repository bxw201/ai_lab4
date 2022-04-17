import re

class Biography:
    def __init__(self, biography: str) -> None:
        sections = biography.split('\n')
        self.name = sections[0].strip()
        self.category = sections[1].lower().strip()
        self.bio = self.process_bio(' '.join(sections[2:]))
    
    @staticmethod
    def stop_words() -> list[str]:
        stop_words = []
        with open('stopwords.txt', 'r') as file:
            for line in file.read().splitlines():
                stop_words += [s for s in line.split(' ') if s != '']
        return stop_words

    def process_bio(self, bio: str) -> list[str]:
        cleaned_bio = re.sub('[^A-Za-z ]+', '', bio.strip()).lower()
        return [s for s in cleaned_bio.split(' ') if (len(s) > 2 and s not in Biography.stop_words())]

    def display(self) -> None:
        print(f'name: {self.name}\ncategory: {self.category}\nbio: {self.bio}')

if __name__ == "__main__":
    s = '''Willa Cather
Writer 
An American author who achieved recognition for her novels of frontier
life on the Great Plains, in works such as O Pioneers, 
My Antonia, and The Song
of the Lark. She was awarded the Pulitzer Prize for One of Ours,
a novel set during World War I.'''
    cather = Biography(s)
    cather.display()