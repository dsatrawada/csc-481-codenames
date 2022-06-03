from wn_cache import WnCacheWriter
import sys, os
import re
import json

import nltk
import json
from nltk.corpus import wordnet as wn
nltk.download('wordnet')
nltk.download('omw-1.4')

from tqdm import tqdm

class MerCacheWriter(WnCacheWriter):

    def __init__(
            self, 
            word_bank_path: str, 
            board_bank_path: str,
            cache_name: str):

        super(MerCacheWriter, self).__init__(
                                        word_bank_path,
                                        board_bank_path,
                                        cache_name)


    def synset_similarity(self, syn1, syn2) -> float:
        '''
        If we are to define another type of similarity between synsets
        you extend this class and redefine this funtion
        '''
        if syn2 in syn1.member_meronyms() or \
            syn2 in syn1.part_meronyms() or \
            syn2 in syn1.substance_meronyms() or \
            syn2 in syn1.member_holonyms() or \
            syn2 in syn1.part_holonyms() or \
            syn2 in syn1.substance_holonyms():
            return 1.0
        return 0

def main():
    word_bank_loc = os.path.join('..', '..', 'words', 'word_bank.txt')
    board_bank_loc = os.path.join('..', '..', 'words', 'board_bank.txt')

    hpycw = MerCacheWriter(word_bank_loc, board_bank_loc, 'test_mer_holo.json')
    hpycw.create_cache()

if __name__ == '__main__':
    main()
        
