import sys, os
import re
import json

from tqdm import tqdm
import numpy as np
from collections import Counter
import numpy as np

from cache import CacheWriter


class D2VCacheWriter(CacheWriter):

    def __init__(
            self, 
            word_bank_path: str, 
            board_bank_path: str,
            cache_name: str,
            vec_path: str):
        '''
        :param: vec_path: path to pre-learned vectors from dict2vec
        '''

        # self.word_bank_path = ''
        super(D2VCacheWriter, self).__init__(
                                        word_bank_path,
                                        board_bank_path,
                                        cache_name)
        self.word_set = set(self.wbw + self.bbw)
        self.vec_dict = self.read_vec_file(vec_path)

    def read_vec_file(self, vec_path):
        '''
        Creates a dictionary from a word to a np array with the vector
        for the word
        '''
        ret_dict = {}
        with open(vec_path, 'r') as fin:
            for line in fin.readlines():
                tokens = line.split()
                if tokens[0] not in self.word_set:
                    continue
                word = tokens[0]
                nums = np.array([float(w) for w in tokens[1:]])
                ret_dict[word] = nums
        return ret_dict 


    def base_similarity(self, w1: str, w2: str) -> float:
        '''
        Calculates the similarity between word 1 and word 2.

        Returns the min, max, avg similarity between the two
        words. For synsets this is well defined as the min, max
        and average of the similarities bewtween the cross product
        of the synsets. For words, this should just return the same
        value three times
        ''' 

        '''Word2Vec model approach to retrieving cosine distances between words. Not working as expected at the moment''' 
        v1 = self.vec_dict[w1]
        v2 = self.vec_dict[w2]
        v1_mag = np.sqrt(v1 @ v1)
        v2_mag = np.sqrt(v2 @ v2)
        return (v1 @ v2) / (v1_mag * v2_mag)


if __name__ == '__main__':
    word_bank_loc = os.path.join('..', '..', 'words', 'word_bank.txt')
    board_bank_loc = os.path.join('..', '..', 'words', 'board_bank.txt')
    dict2vec_loc = os.path.join('..', '..', 'data', 'dict2vec-100d.vec')

    w2vcw = D2VCacheWriter(word_bank_loc, board_bank_loc, 'd2v_sim.json', dict2vec_loc)
    w2vcw.create_cache()
