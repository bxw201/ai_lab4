'''
Module contains class Biography
'''

import re

class Biography:
    '''
    Represents the information in a given biography
    Properties:
    name - name of the person
    category - category in which they belong to
    bio - the full biographical text associated with the person
    words - the set of words in the biography, exclluding stop words
    '''
    def __init__(self, biography: str) -> None:
        sections = biography.split('\n')
        self.name = sections[0].strip()
        self.category = sections[1].lower().strip()
        self.bio = ' '.join(sections[2:])
        self.process_bio()

    @staticmethod
    def stop_words() -> list[str]:
        '''
        Returns the list of stopwords gathered from stopwords.txt
        '''
        stop_words = []
        with open('stopwords.txt', 'r', encoding='utf-8') as file:
            for line in file.read().splitlines():
                stop_words += [s for s in line.split(' ') if s != '']
        return stop_words

    def process_bio(self) -> list[str]:
        '''
        Takes the biography string and sets self.words to be the set
            of important words in the biography
        Excludes stop words and words less than two characters long
        '''
        cleaned_bio = re.sub('[^A-Za-z ]+', '', self.bio.strip()).lower()
        bio_word_list = [s for s in cleaned_bio.split(' ') \
            if (len(s) > 2 and s not in Biography.stop_words())]
        self.words = set(bio_word_list)

    def display(self) -> None:
        '''
        Prints the class to the console
        '''
        print(f'name: {self.name}\ncategory: {self.category}\nbio: {self.words}')

if __name__ == "__main__":
    BIO_STRING = '''Willa Cather
Writer 
An American author who achieved recognition for her novels of frontier
life on the Great Plains, in works such as O Pioneers, 
My Antonia, and The Song
of the Lark. She was awarded the Pulitzer Prize for One of Ours,
a novel set during World War I.'''
    cather = Biography(BIO_STRING)
    cather.display()
