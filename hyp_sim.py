import sys, os

# import re
# import nltk
import json
# from nltk.corpus import wordnet as wn
# nltk.download('wordnet')
# nltk.download('omw-1.4')

# from tqdm import tqdm


class HypernymSimilarity:

    def __init__(self, cache_loc=None):
        '''
        Given two words, this class provides means to find the similarity between
        them by searching in a hash map. The hash map is stored locally in a json
        file. To create the json file, run the main method of this module. The file
        takes around 1.5 hrs to create.
        :param cache_loc: path to the file where the similarities are stored
        '''
        # Contains a mapping between two words joined by
        # an '_' to their similarity score
        self.sym_map = {}
        self.cache_loc = cache_loc
        if self.cache_loc is None:
            self.cache_loc = os.path.join('similarities', 'hyp.json')
        self.sym_map = self.load_map()


    def similarity(self, w1: str, w2: str, sim_type: str)  -> float:
        '''
        Returns the Hypernym Similarity between word1 and
        word2. 
        :param w1: first word of the pair.
        :param w2: second word of the pair.
        :param sim_type: One of 'min', 'max', or 'avg'. Given two words, this can
            either return the min, max, or average between the many possible pairs of 
            synsets between the words
        :returns a float representing the similarity between 
            the two words
        '''
        key = gen_id(w1, w2) 
        if key in self.sym_map:
            if sim_type == 'avg':
                return self.sym_map[key]['avg']
            if sim_type == 'min':
                return self.sym_map[key]['min']
            if sim_type == 'max':
                return self.sym_map[key]['max']
        raise ValueError('Similarity between ' + w1 + ' and ' + w2 + ' not found.' + \
                'Consider refreshing the cache by running the main method of hyp_sim.py')

    def load_map(self) -> dict[str, dict[str, float]]:
        '''
        Loads the hypernym similarity map from a stored file
        '''
        with open(self.cache_loc, 'r') as fin:
            return json.load(fin)


def gen_id(str1, str2):
    '''
    Protocol for storing the similarity between pairs of strings. 
    '''
    if str1 < str2:
        return str1 + '_' + str2
    return str2 + '_' + str1

syn_sim = {} # Global Variable keeping track of similarities between synsets
def base_similarity(w1: str, w2: str) -> float:
    '''
    Calculates the similaritye between word 1 and word 2
    by using the built in wordnet functionality.

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
            syn_id = gen_id(syn1_id, syn2_id)
            if syn_id in syn_sim:
                similarity = syn_sim[syn_id]
            else:
                similarity = syn1.path_similarity(syn2)
                syn_sim[syn_id] = similarity
            sim_sum += similarity 
            sim_count += 1
            if similarity < sim_min:
                sim_min = similarity
            if similarity > sim_max:
                sim_max = similarity
    return sim_sum / sim_count, sim_min, sim_max
    

# def create_cache(word_bank: str, board_bank: str) -> None:
#     '''
#     Creates the similarity cache for Hypernym_Similarity
#     :param word_bank: file name of the overall word bank
#     :param board_bank: file name of the boark bank of words
#     '''
#     cache_loc = 'similarities'
#     if not os.path.exists(cache_loc):
#         os.makedirs(cache_loc)
#     with open(word_bank, 'r') as fin:
#         wb_contents = fin.read()
#     with open(board_bank, 'r') as fin:
#         bb_contents = fin.read()
#     wbw = re.findall(r'[A-z]+', wb_contents)
#     bbw = re.findall(r'[A-z]+', bb_contents)

#     sim = {}
#     for w1 in tqdm(wbw):
#         for w2 in bbw:
#             str_id = gen_id(w1, w2)
#             if str_id in sim:
#                 continue
#             sim[str_id] = {}
#             avg_sim, min_sim, max_sim = base_similarity(w1, w2)
#             sim[str_id]['avg'] = avg_sim
#             sim[str_id]['min'] = min_sim
#             sim[str_id]['max'] = max_sim

#     with open(os.path.join(cache_loc, 'hyp.json'), 'w') as fout:
#         fout.write(json.dumps(sim))


# if __name__ == '__main__':
#     if len(sys.argv) < 2:
#         word_bank = os.path.join('words', 'word_bank.txt')
#     else:
#         word_bank = sys.argv[1]

#     if len(sys.argv) < 3:
#         board_bank = os.path.join('words', 'board_bank.txt')
#     else:
#         board_bank = sys.argv[2]
#     create_cache(word_bank, board_bank)



    



