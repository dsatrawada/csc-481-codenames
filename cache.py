import sys, os
import re
import json

from tqdm import tqdm



class CacheWriter:

    def __init__(
            self, 
            word_bank_path: str, 
            board_bank_path: str,
            cache_name: str):

         with open(word_bank_path, 'r') as fin:
             wb_contents = fin.read()
         with open(board_bank_path, 'r') as fin:
             bb_contents = fin.read()
         self.wbw = re.findall(r'[A-z]+', wb_contents)
         self.bbw = re.findall(r'[A-z]+', bb_contents)

         cache_loc = 'similarities'
         if not os.path.exists(cache_loc):
             os.makedirs(cache_loc)

         self.cache_path = os.path.join(cache_loc, cache_name)


    def gen_id(str1, str2):
        '''
        Protocol for storing the similarity between pairs of strings. 
        '''
        if str1 < str2:
            return str1 + '_' + str2
        return str2 + '_' + str1


    def base_similarity(self, w1: str, w2: str) -> float:
        '''
        Calculates the similarity between word 1 and word 2.

        Returns the min, max, avg similarity between the two
        words. For synsets this is well defined as the min, max
        and average of the similarities bewtween the cross product
        of the synsets. For words, this should just return the same
        value three times
        '''
        return 0, 0, 0
        

    def create_cache(self) -> None:
        '''
        Creates the similarity cache for Hypernym_Similarity
        :param word_bank: file name of the overall word bank
        :param board_bank: file name of the boark bank of words
        '''

        sim = {}
        for w1 in tqdm(self.wbw):
            for w2 in self.bbw:
                str_id = CacheWriter.gen_id(w1, w2)
                if str_id in sim:
                    continue
                sim[str_id] = {}
                avg_sim, min_sim, max_sim = self.base_similarity(w1, w2)
                sim[str_id]['avg'] = avg_sim
                sim[str_id]['min'] = min_sim
                sim[str_id]['max'] = max_sim

        with open(self.cache_path, 'w') as fout:
            fout.write(json.dumps(sim))


if __name__ == '__main__':
    word_bank_loc = os.path.join('words', 'word_bank.txt')
    board_bank_loc = os.path.join('words', 'board_bank.txt')

    cw = CacheWriter(word_bank_loc, board_bank_loc, 'test.json')
    cw.create_cache()
