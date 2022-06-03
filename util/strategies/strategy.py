import os
import re
from typing import Tuple

import numpy as np
from util.loss import loss
from util.similarity import Similarity


class Strategy:

    def __init__(self, cache_file):
        """
        :param cache_loc: path to the file where the similarities are stored (ex: ant.json)
        """
        self.sim = Similarity(cache_file)
        # Load the wordbank
        word_bank = os.path.join('words', 'word_bank.txt')
        with open(word_bank, 'r') as fin:
            wb_contents = fin.read()
        wbw = re.findall(r'[A-z]+', wb_contents)
        self.wordbank = wbw

    def calculate_similarity(self, w1: str, w2: str) -> float:
        """
        Calculate the similarity between two words
        :param w1: the first word
        :param w2: the second word
        :return a float between 0 and 1 representing the similarity between two words
        """
        return self.sim.similarity(w1, w2)

    def find_clue(
        self, words: set[str], a_words: set[str], o_words: set[str],
            n_words: set[str], d_words: set[str], cant_use: set[str]) -> Tuple[str, int]:
        """
        Look up the wordbank and find the best clue 
        :param words: Words on the board.
        :param a_words: Agent words. We want to guess these words.
        :param o_words: Opponent words. 
        :param n_words: Neutral words. 
        :param d_words: Assasin words.
        :param cant_use: Words that are either one of the 25 starting words, or hints that have been given
        :return: (The best clue, the words we expect to be guessed)
        """
        print("Thinking...")
        max_score = (None, float('inf') * -1,
                     float('-inf') * -1)  # (Word, Optimal Loss Score, # of guesses to be used)
        # n = 0
        for word in self.wordbank:

            if word in cant_use or  word in words:
                continue
            a_sim = []
            o_sim = []
            n_sim = []
            d_sim = []
            for a_word in a_words:
                a_sim.append(self.calculate_similarity(word, a_word))

            for o_word in o_words:
                o_sim.append(self.calculate_similarity(word, o_word))

            for n_word in n_words:
                n_sim.append(self.calculate_similarity(word, n_word))

            for d_word in d_words:
                d_sim.append(self.calculate_similarity(word, d_word))

            score_list = loss(3, a_sim, o_sim,
                              n_sim, d_sim[0], lambda x: np.exp(10*x))
            # print(word, score_list)
            current_max = max(score_list)
            max_index = [index for index, item in enumerate(
                score_list) if item == current_max][0] + 1
            if current_max > max_score[1]:
                max_score = (word, current_max, max_index)

        return (max_score[0], max_score[2])

    def make_guess(self, clue: str, words: list[str]) -> str:
        """
        From a given clue, choosing the guess that are most similar to the clue
        :param clue: The given clue
        :param words: Available words in the board to choose
        """

        max_sim = float('inf') * -1
        word_chosen = "None"
        for word in words:
            sim = self.calculate_similarity(word, clue)
            if sim > max_sim:
                sim = max_sim
                word_chosen = word
        return word_chosen
