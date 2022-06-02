import sys, os
import re
import json

from tqdm import tqdm
import numpy as np
from gensim.models import Word2Vec
from collections import Counter
from math import sqrt

from cache import CacheWriter


class W2VCacheWriter(CacheWriter):

    def __init__(
            self, 
            word_bank_path: str, 
            board_bank_path: str,
            cache_name: str):

        # self.word_bank_path = ''
        super(W2VCacheWriter, self).__init__(
                                        word_bank_path,
                                        board_bank_path,
                                        cache_name)

    def w2c(self, word: str) -> tuple[dict,set,float]:

        word_dict = {}

        for c in word:
            if c in word_dict:
                word_dict[c] += 1
            else:
                word_dict[c] = 1
        
        word_set = set(word_dict.keys())

        vec_len = sqrt(sum(char*char for char in word_dict.values()))

        return word_dict, word_set, vec_len

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
        # words = open('word_bank.txt', 'r')
        # list_of_words = [line.split(',') for line in words.readlines()]
        # model = Word2Vec(list_of_words, size=150, window=10, min_count=2, workers=10)
        # model.train(list_of_words,total_examples=len(list_of_words),epochs=10)
        # cosine_similarity = np.dot(model[w1], model[w2])/(np.linalg.norm(model[w1])*np.linalg.norm(model[w2]))
        # return cosine_similarity, cosine_similarity, cosine_similarity

        vec1 = self.w2c(w1)
        vec2 = self.w2c(w2)

        common_chars = vec1[1].intersection(vec2[1])

        distance = sum(vec1[0][char]*vec2[0][char] for char in common_chars)/vec1[2]/vec2[2]

        return distance, distance, distance

    




if __name__ == '__main__':
    word_bank_loc = os.path.join('words', 'word_bank.txt')
    board_bank_loc = os.path.join('words', 'board_bank.txt')

    w2vcw = W2VCacheWriter(word_bank_loc, board_bank_loc, 'w2vtest.json')
    w2vcw.create_cache()
    # w1 = 'manager'
    # w2 = 'management'

    # w2v = W2VCacheWriter('','', '')

    # print(w2v.base_similarity(w1,w2))
