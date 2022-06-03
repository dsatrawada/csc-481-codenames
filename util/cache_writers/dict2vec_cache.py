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
        super(W2VCacheWriter, self).__init__(
                                        word_bank_path,
                                        board_bank_path,
                                        cache_name)
        self.vec_dict = self.read_vec_file(vec_path)
        self.word_set = set(self.wbw + self.bbw)

    def read_vec_file(self):
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
    word_bank_loc = os.path.join('..', '..', 'words', 'word_bank.txt')
    board_bank_loc = os.path.join('..', '..', 'words', 'board_bank.txt')

    w2vcw = W2VCacheWriter(word_bank_loc, board_bank_loc, 'w2vtest.json')
    w2vcw.create_cache()
    # w1 = 'manager'
    # w2 = 'management'

    # w2v = W2VCacheWriter('','', '')

    # print(w2v.base_similarity(w1,w2))
