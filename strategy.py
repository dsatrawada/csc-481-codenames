
from typing import  Tuple

class Strategy:
    
    def __init__(self) :
        pass


    def find_clue(
        self, words: set[str], a_words: set[str], o_words: set[str],
            n_words: set[str], d_words: set[str], cant_use: set[str]) -> Tuple[str, int]:
        """
        :param words: Words on the board.
        :param my_words: Words we want to guess.
        :param black_list: Clues we are not allowed to give.
        :return: (The best clue, the score, the words we expect to be guessed)
        """
        raise NotImplementedError


    # def loss(max_words: int, a_sim: Iterable[float], o_sim: Iterable[float], 
    #         n_sim: Iterable[float], l_sim: float) -> Iterable[float]:
    #     """
    #     Given similarities between a word and a board, return a list of expected
    #     change in cards given that the guess applies to 1, 2, ... max_words cards
    #     :param max_words: number of words a hint applies to. The depth of the 
    #         simulation tree will then be min(max_words + 1, len(a_sim))
    #     :param a_sim: list of similarities between the guess, and each agent word
    #     :param o_sim: list of similarities between the guess, and each oponent word
    #     :param n_sim: list of similarities between the guess, and each neutral word
    #     :param l_sim: similarity between the guess and the assasin word
    #     """
    #     raise NotImplementedError

  