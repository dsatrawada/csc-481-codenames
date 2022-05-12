
from typing import List, Tuple, Iterable


class Strategy:
    
    def __init__(self) -> Strategy:
        """
        """
        pass


    def find_clue(
        self, words: set[str], a_words: set[str], o_words: set[str],
            n_words: set[str], d_words: set[str], black_list: set[str]) -> Tuple[str, float, List[str]]:
        """
        :param words: Words on the board.
        :param my_words: Words we want to guess.
        :param black_list: Clues we are not allowed to give.
        :return: (The best clue, the score, the words we expect to be guessed)
        """
        return (None, 0, [None])
