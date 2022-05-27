import sys, os
import re
import json

import nltk
import json
from nltk.corpus import wordnet as wn
nltk.download('wordnet')
nltk.download('omw-1.4')

from tqdm import tqdm
from cache import CacheWriter

class WnCacheWriter(CacheWriter):

    def __init__(
            self, 
            word_bank_path: str, 
            board_bank_path: str,
            cache_name: str):

        super(WnCacheWriter, self).__init__(
                                        word_bank_path,
                                        board_bank_path,
                                        cache_name)
        self.syn_sim = {}


    def synset_similarity(self, syn1, syn2) -> float:
        '''
        If we are to define another type of similarity between synsets
        you extend this class and redefine this funtion
        '''
        return 0.5 


    def base_similarity(self, w1: str, w2: str) -> float:
        '''
        Calculates the similaritye between word 1 and word 2.

        For now we can just take the min, max, and average of the simlarity
        between all senses of the synsets of the words. We will keep track
        of the pairs of synsets that we've already computed in a global
        variable so we don't compute them again
        '''
        global syn_sim
        w1_synsets = wn.synsets(w1)
        w2_synsets = wn.synsets(w2)
        sim_sum = 0
        sim_count = 0
        sim_min = 100
        sim_max = -1
        for syn1 in w1_synsets:
            syn1_id = str(syn1.offset())
            for syn2 in w2_synsets:
                syn2_id = str(syn2.offset())
                syn_id = CacheWriter.gen_id(syn1_id, syn2_id)
                if syn_id in self.syn_sim:
                    similarity = self.syn_sim[syn_id]
                else:
                    similarity = self.synset_similarity(syn1, syn2) 
                    self.syn_sim[syn_id] = similarity
                sim_sum += similarity 
                sim_count += 1
                if similarity < sim_min:
                    sim_min = similarity
                if similarity > sim_max:
                    sim_max = similarity
        return sim_sum / sim_count, sim_min, sim_max

def main():
    word_bank_loc = os.path.join('words', 'word_bank.txt')
    board_bank_loc = os.path.join('words', 'board_bank.txt')

    wncw = WnCacheWriter(word_bank_loc, board_bank_loc, 'test.json')
    wncw.create_cache()

if __name__ == '__main__':
    main()
        
