from cache import CacheWriter
import sys, os
import re
import json

import nltk
import json
from nltk.corpus import wordnet as wn
nltk.download('wordnet')
nltk.download('omw-1.4')

from tqdm import tqdm

class AntCacheWriter(CacheWriter):

    def __init__(
            self, 
            word_bank_path: str, 
            board_bank_path: str,
            cache_name: str):

        super(AntCacheWriter, self).__init__(
                                        word_bank_path,
                                        board_bank_path,
                                        cache_name)

    def base_similarity(self, w1: str, w2: str) -> float:
        '''
        Calculates the similarity between word 1 and word 2.

        Returns the min, max, avg similarity between the two
        words. For synsets this is well defined as the min, max
        and average of the similarities bewtween the cross product
        of the synsets. For words, this should just return the same
        value three times
        '''
        for lemma in wn.lemmas(w1):
            for antonym in lemma.antonyms():
                if antonym in wn.lemmas(w2):
                    return 1.0, 1.0, 1.0

        return 0, 0, 0
        
def main():
    word_bank_loc = os.path.join('..', '..', 'words', 'word_bank.txt')
    board_bank_loc = os.path.join('..', '..', 'words', 'board_bank.txt')

    antcw = AntCacheWriter(word_bank_loc, board_bank_loc, 'ant.json')
    antcw.create_cache()

if __name__ == '__main__':
    main()
        
