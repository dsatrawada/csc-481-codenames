import sys, os

import json

from similarity import Similarity

class MeronymHolonymSimilarity(Similarity):
    def __init__(self, similarity_type: str, cache_loc=None):
        '''
        Given two words, this class provides means to find the similarity between
        them by searching in a hash map. The hash map is stored locally in a json
        file. To create the json file, run the main method of this module. The file
        takes around 1.5 hrs to create.
        :param similarity_type: one of 'min', 'max', or 'avg'. Returns the min, max
            or avg similarity between synsets
        :param cache_loc: path to the file where the similarities are stored
        '''
        super(MeronymHolonymSimilarity, self).__init__()
        self.sym_map = {}
        self.cache_loc = cache_loc
        if self.cache_loc is None:
            self.cache_loc = os.path.join('similarities', 'mer_holo.json')
        self.sym_map = self.load_map()
        self.similarity_type = similarity_type


    def similarity(self, w1: str, w2: str)  -> float:
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
            if self.similarity_type == 'avg':
                return self.sym_map[key]['avg']
            if self.similarity_type == 'min':
                return self.sym_map[key]['min']
            if self.similarity_type == 'max':
                return self.sym_map[key]['max']
        raise ValueError('Similarity between ' + w1 + ' and ' + w2 + ' not found.' + \
                'Consider refreshing the cache by running the main method of hyp_sim.py')

    def load_map(self) -> dict[str, dict[str, float]]:
        '''
        Loads the hypernym similarity map from a stored file
        '''
        with open(self.cache_loc, 'r') as fin:
            return json.load(fin)
    

# if __name__ == '__main__':
#     hs = HypernymSimilarity('min', os.path.join('similarities', 'w2vtest.json'))
#     print(hs.similarity('worm', 'have'))





