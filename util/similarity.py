import sys
import os

import json
from util.cache_writers.cache import CacheWriter


class Similarity():
    def __init__(self, similarity_type: str, cache_file):
        '''
        Given two words, this class provides means to find the similarity between
        them.
        :param similarity_type: one of 'min', 'max', or 'avg'. Returns the min, max
            or avg similarity between synsets
        :param cache_loc: path to the file where the similarities are stored
        '''
        self.sym_map = {}
        self.cache_loc = os.path.join(
            'similarities', cache_file)
        self.sym_map = self.load_map()
        self.similarity_type = similarity_type

    def similarity(self, w1: str, w2: str) -> float:
        '''
        Returns the Hypernym Similarity between word1 and
        word2. 
        :param w1: first word of the pair.
        :param w2: second word of the pair.
        :returns a float representing the similarity between 
            the two words
        '''
        key = self.gen_id(w1, w2)
        if key in self.sym_map:
            return self.sym_map[key]
        raise ValueError('Similarity between ' + w1 + ' and ' + w2 + ' not found.' +
                         'Consider refreshing the cache by running the main method of the corresponding cache file.')

    def load_map(self):
        '''
        Loads the similarity map from a stored file
        '''
        with open(self.cache_loc, 'r') as fin:
            return json.load(fin)

    def gen_id(self, w1: str, w2: str) -> str:
        '''
        Get a string id for the two words based on the function
        implemented by CacheWriter
        :param w1: Fisrt word
        :param w2: Second word
        :returns: string representing the id
        '''
        return CacheWriter.gen_id(w1, w2)
