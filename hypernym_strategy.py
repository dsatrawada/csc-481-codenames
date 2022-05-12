
from typing import List, Tuple, Iterable
from nltk.corpus import wordnet as wn


class HypernymStrategy(Strategy):
    """
    The HypernymStrategy class extends the Strategy class and searches for clues
    by examining only hypernym relationships. 
    """
    
    def __init__(self, h0: float, h1: float, h2: float, h3: float) -> HypernymStrategy:
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


    def find_clue(
        self, words: set[str], a_words: set[str], o_words: set[str],
            n_words: set[str], d_words: set[str], cant_use: set[str]) -> Tuple[str, float, List[str]]:
        """
        :param words: Words on the board.
        :param a_words: Agent words. We want to guess these words.
        :param o_words: Opponent words. 
        :param n_words: Neutral words. 
        :param d_words: Assasin words.
        :param cant_use: Words that are one one of the 25 starting words, or hints that
            have been given
        :return: (The best clue, the score, the words we expect to be guessed)
        """

    def get_utility(self, i_sim: list[int], o_sim: list[int], a_sim: int):
        """
        :param i_sim: List of path lengths between target words and a guess.
        :param o_sim: List of path lengths between a guess and oponent words.
        :param a_sim: Path lenght between a guess and the assassin word
        """
        return h0 * len(i_sim) + h1 * max(i_sim) - h2 * min(o_sim)


