
import os
import re
from typing import Tuple
from util.strategies.strategy import Strategy
from util.similarities.hyp_similarity import HypernymSimilarity
from util.similarities.mer_holo_similarity import MeronymHolonymSimilarity
from util.loss import loss
import numpy as np

class CombinedStrategy(Strategy):
    """
    The CombineStrategy class extends the Strategy class and searches for clues
    by examining meronym +holonym, combined with hyper/hyponym relationships. 
    """

    def __init__(self, h0: float, h1: float, h2: float, h3: float):
        """
        :param h0: Weight for the number of words in a guess
        :param h1: Weight for the maximum similarity loss of the guess and the
            target set of words. A larger similarity loss indicates lower similarity
        :param h2: Weight for the minimum similarity loss of the guess and an opponent
            word.
        :param h3: Weight for the similarityu loss of the guess and the assassin word
        """
        super().__init__()
        self.h0 = h0
        self.h1 = h1
        self.h2 = h2
        self.h3 = h3
        self.hs = HypernymSimilarity("max")
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
                sim = self.hs.similarity(word, a_word)*0.8 + self.ms.similarity(word, a_word) * 0.2
                a_sim.append(sim)

            for o_word in o_words:
                sim = self.hs.similarity(word, o_word)*0.8 + self.ms.similarity(word, o_word) * 0.2
                o_sim.append(sim)

            for n_word in n_words:
                sim = self.hs.similarity(word, n_word)*0.8 + self.ms.similarity(word, n_word) * 0.2
                n_sim.append(sim)

            for l_word in d_words:
                sim = self.hs.similarity(word, l_word)*0.8 + self.ms.similarity(word, l_word) * 0.2
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

    # def get_utility(self, i_sim: list[int], o_sim: list[int], a_sim: int):
    #     """
    #     :param i_sim: List of path lengths between target words and a guess.
    #     :param o_sim: List of path lengths between a guess and oponent words.
    #     :param a_sim: Path lenght between a guess and the assassin word
    #     """
    #     return h0 * len(i_sim) + h1 * max(i_sim) - h2 * min(o_sim)
