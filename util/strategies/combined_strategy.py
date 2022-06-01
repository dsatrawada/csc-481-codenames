
import os
import re
from typing import Tuple
from util.strategies.strategy import Strategy
from util.similarities.hyp_similarity import HypernymHyponymSimilarity
from util.similarities.mer_holo_similarity import MeronymHolonymSimilarity
from util.loss import loss
import numpy as np

class CombinedStrategy(Strategy):
    """
    The CombineStrategy class extends the Strategy class and searches for clues
    by examining meronym +holonym, combined with hyper/hyponym relationships. 
    """

    def __init__(self, h0: float, h1: float, h2: float):
        """
        :param h0: Weight for the hyponym-hypernym similarity
        :param h1: Weight for the meronym-holonym similarity
        :param h2: Weight for the antonym similarity
        """
        super().__init__()
        self.h0 = h0
        self.h1 = h1
        self.h2 = h2
      
        self.hs = HypernymHyponymSimilarity("max")
        self.ms = MeronymHolonymSimilarity("max")
        # Load the wordbank
        word_bank = os.path.join('words', 'word_bank.txt')
        with open(word_bank, 'r') as fin:
            wb_contents = fin.read()
        wbw = re.findall(r'[A-z]+', wb_contents)
        self.wordbank = wbw

    def find_clue(
        self, words: set[str], a_words: set[str], o_words: set[str],
            n_words: set[str], d_words: set[str], cant_use: set[str]) -> Tuple[str, int]:
        """
        :param words: Words on the board.
        :param a_words: Agent words. We want to guess these words.
        :param o_words: Opponent words. 
        :param n_words: Neutral words. 
        :param d_words: Assasin words.
        :param cant_use: Words that are one one of the 25 starting words, or hints that
            have been given
        :return: (The best clue, the words we expect to be guessed)
        """
        print("Thinking...")
        max_score = (None, float('inf')* -1,
                     float('-inf') * -1)  # (Word, Optimal Loss Score, # of guesses to be used)
        # n = 0
        for word in self.wordbank:

            if word in words or word in cant_use:
                continue
            a_sim = []
            o_sim = []
            n_sim = []
            l_sim = []
            for a_word in a_words:
                # sim = self.hs.similarity(word, a_word)*self.h0 + self.ms.similarity(word, a_word) * self.h1
                sim = max(self.hs.similarity(word, a_word), self.ms.similarity(word, a_word))
                a_sim.append(sim)

            for o_word in o_words:
                # sim = self.hs.similarity(word, o_word)*self.h0 + self.ms.similarity(word, o_word) * self.h1
                sim = max(self.hs.similarity(word, o_word), self.ms.similarity(word, o_word))
                o_sim.append(sim)

            for n_word in n_words:
                # sim = self.hs.similarity(word, n_word)*self.h0 + self.ms.similarity(word, n_word) * self.h1
                sim = max(self.hs.similarity(word, n_word), self.ms.similarity(word, n_word))
                n_sim.append(sim)

            for l_word in d_words:
                # sim = self.hs.similarity(word, l_word)*self.h0 + self.ms.similarity(word, l_word) * self.h1
                sim = max(self.hs.similarity(word, l_word), self.ms.similarity(word, l_word))
                l_sim.append(sim)
            
            
            score_list = loss(3, a_sim, o_sim,
                              n_sim, l_sim[0], lambda x: np.exp(10*x))
            # print(word, score_list)
            current_max = max(score_list)
            max_index = [index for index, item in enumerate(
                score_list) if item == current_max][0] + 1
            if current_max  > max_score[1] :
                max_score = (word, current_max, max_index)

        return (max_score[0], max_score[2])

  

    def make_guess(self, clue: str, words: list[str]) -> str:
        max_sim = float('inf')* -1;
        word_chosen = "None"
        for word in words:
            # sim = self.hs.similarity(word, clue)*self.h0 + self.ms.similarity(word, clue) * self.h1
            sim = max(self.hs.similarity(word, clue) , self.ms.similarity(word, clue) * self.h1)
            if sim > max_sim:
                sim = max_sim
                word_chosen = word
        return word_chosen