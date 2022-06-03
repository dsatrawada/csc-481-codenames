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

    def get_syn_weights(self, w: str) -> list[tuple[nltk.corpus.reader.wordnet.Synset, float]]:
        '''
        Return a dictionary with the synset_offset as the 
        key and the probability that the sysnet will be 
        associated with the word as the value
        '''
        tot_weights = 1e-6
        ret_syns = []
        for syn in wn.synsets(w):
            word_weight = 0
            for lem in syn.lemmas():
                if lem.name().lower() == w:
                    word_weight = lem.count()
            tot_weights += word_weight 
            ret_syns.append([syn, word_weight]) 

        ret_tups = []
        for i in range(len(ret_syns)):
            ret_syns[i][1] /= tot_weights
            ret_tups.append((ret_syns[i][0], ret_syns[i][1]))
        return ret_tups 


    def base_similarity(self, w1: str, w2: str) -> float:
        '''
        Calculates the similaritye between word 1 and word 2.

        For now we can just take the min, max, and average of the simlarity
        between all senses of the synsets of the words. We will keep track
        of the pairs of synsets that we've already computed in a global
        variable so we don't compute them again
        '''
        global syn_sim

        syn1_weights = self.get_syn_weights(w1)
        syn2_weights = self.get_syn_weights(w2)


        result = 0
        for syn1, weight1 in syn1_weights:
            syn1_id = str(syn1.offset())
            for syn2, weight2 in syn2_weights:
                syn2_id = str(syn2.offset())
                syn_id = CacheWriter.gen_id(syn1_id, syn2_id)
                if syn_id in self.syn_sim:
                    similarity = self.syn_sim[syn_id]
                else:
                    similarity = self.synset_similarity(syn1, syn2) 
                    self.syn_sim[syn_id] = similarity
                result += (weight1 * weight2 * similarity)
        return result 

def main():
    word_bank_loc = os.path.join('words', 'word_bank.txt')
    board_bank_loc = os.path.join('words', 'board_bank.txt')

    wncw = WnCacheWriter(word_bank_loc, board_bank_loc, 'test.json')
    wncw.create_cache()

if __name__ == '__main__':
    main()
        
