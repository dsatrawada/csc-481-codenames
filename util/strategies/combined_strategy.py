
import os
import re
from typing import Tuple
from util.similarity import Similarity
from util.strategies.strategy import Strategy
from util.loss import loss
import numpy as np


class CombinedStrategy(Strategy):
    """
    The CombineStrategy class extends the Strategy class and searches for clues
    by examining meronym/holonym, hypernym/hyponym, and antonym relationships. 
    """

    def __init__(self, name='WordNet', sigma=6):
        super(CombinedStrategy, self).__init__(name=name, sigma=sigma)
        self.hyp = Similarity("hyp.json")
        self.mer = Similarity("mer_holo.json")
        self.ant = Similarity("ant.json")
        # Load the wordbank
        word_bank = os.path.join('words', 'word_bank.txt')
        with open(word_bank, 'r') as fin:
            wb_contents = fin.read()
        wbw = re.findall(r'[A-z]+', wb_contents)
        self.wordbank = wbw

    def calculate_similarity(self, w1, w2):
        
        return max(self.hyp.similarity(w1, w2), self.mer.similarity(
            w1, w2), self.ant.similarity(w1, w2))
