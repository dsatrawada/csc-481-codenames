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

    def make_guess(
            self, clue: str, words: set[str]) -> str:
        """
        :param clue: Clue provided by human spymaster.
        :param words: Words on the board tht have not been revealed.
        :return: The best guess.
        """
        raise NotImplementedError



  

  
    def make_guess(self, clue: str, words: list[str]):
        raise NotImplementedError
    
