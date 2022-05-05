import random
from typing import List, Tuple, Iterable


class Reader:
    def read_picks(
        self, words: List[str], my_words: Iterable[str], cnt: int
    ) -> List[str]:
        """
        Query the user for guesses.
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


class TerminalReader(Reader):
    def read_picks(
        self, words: List[str], my_words: Iterable[str], cnt: int
    ) -> List[str]:
        picks = []
        while len(picks) < cnt:
            guess = None
            while guess not in words:
                guess = input("Your guess: ").strip().upper()
            picks.append(guess)
            if guess in my_words:
                print("Correct!")
            else:
                print("Wrong :(")
                break
        return picks

    def print_words(self, words: List[str], nrows: int):
        longest = max(map(len, words))
        print()
        for row in zip(*(iter(words),) * nrows):
            for word in row:
                print(word.rjust(longest), end=" ")
            print()
        print()


class Codenames:
    def __init__(self, cnt_rows=5, cnt_cols=5, cnt_agents=9, cnt_opponents=8, cnt_neutral=7, cnt_death=1):
        """
        :param cnt_rows: Number of rows to show.
        :param cnt_cols: Number of columns to show.
        :param cnt_agents: Number of agent (player) words.
        :param cnt_opponents: Number of opponent words.
        :param cnt_neutral: Number of neutral words.
        :param cnt_assasin: Number of assasin words.
        """
        self.cnt_rows = cnt_rows
        self.cnt_cols = cnt_cols
        self.cnt_agents = cnt_agents
        self.cnt_opponents = cnt_opponents
        self.cnt_neutral = cnt_neutral
        self.cnt_death = cnt_death

        self.codenames = []

    def load(self, word_bank_file):
        # All words that are allowed to go onto the table
        print("...Loading codenames")

        with open(word_bank_file) as f:
            self.codenames = [line.strip() for line in f]

        print("Ready!")

    def find_clue(
        self, words: List[str], a_words: List[str], o_words: List[str], 
            n_words: List[str], d_words: List[str], black_list: Iterable[str]) -> Tuple[str, float, List[str]]:
        """
        :param words: Words on the board.
        :param my_words: Words we want to guess.
        :param black_list: Clues we are not allowed to give.
        :return: (The best clue, the score, the words we expect to be guessed)
        """
        #TODO

        print("Thinking", end="", flush=True)

        best_clue = "birdie"
        best_guess = ["BADMINTON", "EAGLE"]

        # After printing '.'s with end="" we need a clean line.
        print()

        return best_clue, best_guess

    def play_spymaster(self, reader: Reader):
        """
        Play a complete game, with the robot being the spymaster.
        """
        words = random.sample(self.codenames, self.cnt_rows * self.cnt_cols)
        words_c = words.copy()

        agent_words = set(random.sample(words_c, self.cnt_agents))
        for word in agent_words:
            words_c.remove(word)

        opponent_words = set(random.sample(words_c, self.cnt_opponents))
        for word in opponent_words:
            words_c.remove(word)

        neutral_words = set(random.sample(words_c, self.cnt_neutral))
        for word in neutral_words:
            words_c.remove(word)
        
        d_words = set(random.sample(words_c, self.cnt_death))

        used_clues = set(words)


        while agent_words:
            reader.print_words(words, nrows=self.cnt_rows)

            clue, group = self.find_clue(
                words, list(agent_words), list(opponent_words), list(neutral_words), list(d_words), used_clues)
            # Save the clue, so we don't use it again
            used_clues.add(clue)

            print()
            print(
                'Clue: "{} {}", remaining words {})'.format(
                    clue, len(group), len(agent_words)
                )
            )
            print()
            for pick in reader.read_picks(words, agent_words, len(group)):
                words[words.index(pick)] = "---"
                if pick in agent_words:
                    agent_words.remove(pick)


def main():
    cn = Codenames()
    cn.load("word_bank.txt")
    reader = TerminalReader()
    while True:
        try:
            cn.play_spymaster(reader)
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break


main()
