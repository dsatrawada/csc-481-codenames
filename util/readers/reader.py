from typing import List, Tuple

class Reader:
    def read_picks(
        self, words: List[str], my_words: set[str], opn_words: set[str],
            neutral_words: set[str], d_words: set[str],
            cnt: int
    ) -> None:
        """
        Query the user for guesses and update the board.
        :param words: Words the user can choose from.
        :param my_words: Correct words.
        :param cnt: Number of guesses the user has.
        :return: The words picked by the user.
        """
        raise NotImplementedError

    def print_words(self, words: List[str], nrows: int):
        """
        Prints a list of words as a 2d table, using `nrows` rows.
        :param words: Words to be printed.
        :param nrows: Number of rows to print.
        """
        raise NotImplementedError

    def print_stats(self, my_words: set[str], opn_words: set[str],
                    neutral_words: set[str], d_words: set[str], debug: bool):

        raise NotImplementedError

    def read_clue(self, word_set) -> Tuple[str, int]:
        raise NotImplementedError
