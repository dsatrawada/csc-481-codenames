import sys, os

import json
from util.cache_writers.cache import CacheWriter


class Similarity():
    def __init__(self):
        '''
        Given two words, this class provides means to find the similarity between
        them 
        '''
        pass

    def similarity(self, w1: str, w2: str)  -> float:
        '''
        Returns the Hypernym Similarity between word1 and
        word2. 
        :param w1: first word of the pair.
        :param w2: second word of the pair.
        :returns a float representing the similarity between 
            the two words
        '''
        return 0.1
    
    def gen_id(self, w1: str, w2: str) -> str:
        '''
        Get a string id for the two words based on the function
        implemented by CacheWriter
        :param w1: Fisrt word
        :param w2: Second word
        :returns: string representing the id
        '''
        return CacheWriter.gen_id(w1, w2)




