class Reader:
    def read_picks(
        self, words: list[str], agent_words: set[str], opn_words: set[str],
            neutral_words: set[str], d_words: set[str],
            cnt: int
    ) -> None:
        """
        Query the user for guesses
        :param words: Words the user can choose from.
        :param agent_words: Correct words.
        :param cnt: Number of guesses the user has.
        :return: The words picked by the user.
        """
        raise NotImplementedError

    def print_words(self, words: list[str], nrows: int):
        """
        Prints a list of words as a 2d table, using `nrows` rows.
        :param words: Words to be printed.
        :param nrows: Number of rows to print.
        """
        raise NotImplementedError

    def print_stats(self, agent_words: set[str], opn_words: set[str],
                    neutral_words: set[str], d_words: set[str], revealing: bool):
        """
        Prints the stats for each turn of the game, including the number of 
        remaining agent words (corect words), and remaining  opponent words. 
        When the revealing option is True, this method also prints out
        the comprehensive list of remaining agent words, opponent words, and 
        death words, which is useful when a human is a spymaster. 
        :param agent_words: set of remaining correct words
        :param opn_words: set of opponent words
        :param neutral_words: set of remaining neutral words
        :param d_words: set of remaining assasin (death) words
        :param revealing: revaling option
        """
        raise NotImplementedError

    def read_clue(self, word_set) -> tuple[str, int]:
        """
        Read in and parse a clue provided by the user from the keyboard.
        For calculating word similarity, the user cannot provide a clue 
        that is outside of the wordbank being used in the game
        :param word_set: a set of word in the wordbank. 
        :return: (The clue, the number of words for that clue)
        """
        raise NotImplementedError

    def checkGuess(self, guess: str, words: list[str], agent_words: set[str], opn_words: set[str], neutral_words: set[str], d_words: set[str]) -> bool:
        """
        Validate the guess and update the board accordingly
        :param words: words in the board
        :param agent_words: set of remaining correct words
        :param opn_words: set of remaining opponent words
        :param neutral_words: set of remaining neutral words
        :param d_words: set of remaining assasin (death) words
        :return: True if we make a correct guess, False otherwise
        """
        raise NotImplementedError