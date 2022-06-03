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

    def get_lemma_probs(self, word):
        '''
        Returns a list of tuples where the first value in the 
        tuple is the lemma of a given word, the second value
        is the probability that a word will be taken to mean that lemma
        '''
        probs = []
        sums = 1e-6 
        for lemma in wn.lemmas(word):
            count = lemma.count()
            probs.append([lemma, count])
            sums += count

        tups = []
        for lem_prob in probs:
            tups.append((lem_prob[0], lem_prob[1] / sums))
        return tups



    def base_similarity(self, w1: str, w2: str) -> float:
        '''
        Calculates the similarity between word 1 and word 2.

        Returns the min, max, avg similarity between the two
        words. For synsets this is well defined as the min, max
        and average of the similarities bewtween the cross product
        of the synsets. For words, this should just return the same
        value three times
        '''

        lemprobs1 = self.get_lemma_probs(w1)
        lemprobs2 = self.get_lemma_probs(w2)

        result = 0
        for lem1, prob1 in lemprobs1:
            lem1_ant = set(lem1.antonyms())
            for lem2, prob2 in lemprobs2:
                if lem2 in lem1_ant:
                    result += prob1 * prob2
        return result

        
def main():
    word_bank_loc = os.path.join('..', '..', 'words', 'word_bank.txt')
    board_bank_loc = os.path.join('..', '..', 'words', 'board_bank.txt')

    antcw = AntCacheWriter(word_bank_loc, board_bank_loc, 'test_ant.json')
    antcw.create_cache()

if __name__ == '__main__':
    main()
        
