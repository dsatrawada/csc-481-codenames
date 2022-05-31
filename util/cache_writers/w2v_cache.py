import sys, os
import re
import json

from tqdm import tqdm

from util.cache_writers.cache import CacheWriter


class W2VCacheWriter(CacheWriter):

    def __init__(
            self, 
            word_bank_path: str, 
            board_bank_path: str,
            cache_name: str):

        super(W2VCacheWriter, self).__init__(
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
        return 0.6, 0.6, 0.6


if __name__ == '__main__':
    word_bank_loc = os.path.join('words', 'word_bank.txt')
    board_bank_loc = os.path.join('words', 'board_bank.txt')

    w2vcw = W2VCacheWriter(word_bank_loc, board_bank_loc, 'w2vtest.json')
    w2vcw.create_cache()
