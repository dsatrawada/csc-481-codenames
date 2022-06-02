import os
import random
from typing import List, Tuple
import re
from util.strategies.strategy import Strategy
from util.strategies.combined_strategy import CombinedStrategy

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
                    neutral_words: set[str], d_words: set[str], revealing: bool):

        raise NotImplementedError

    def read_clue(self, word_set) -> Tuple[str, int]:
        raise NotImplementedError



class TerminalReader(Reader):
    def read_picks(
        self, words: List[str], my_words: set[str], opn_words: set[str],
        neutral_words: set[str], d_words: set[str],
        cnt: int
    ) -> None:
        picksCount = 0
        while True:
            guess = None
            while guess not in words or guess in {"-O-", "-N-", "-✓-"}:
                guess = input("Your guess (P to pass): ").strip()
                if guess == 'P':
                    print("\nPass...\n")
                    return 

            if guess in my_words:
                print("\nCorrect!\n")
                my_words.remove(guess)
                words[words.index(guess)] = "-✓-"
                picksCount += 1
            else:
                if guess in d_words:
                    print("\nWrong - Assassin Word x_x\n")
                    exit(0)

                if guess in neutral_words:
                    print("\nWrong - Neutral Word :(\n")
                    neutral_words.remove(guess)
                    words[words.index(guess)] = "-N-"
                    break

                if guess in opn_words:
                    print("\nWrong - Opponent Word :(\n")
                    opn_words.remove(guess)
                    words[words.index(guess)] = "-O-"
                    break
                

            if (picksCount >= cnt):
                print("\nNo more attempts\n")
                break


    def read_clue(self, word_set) -> Tuple[str, int]:
        while True:
            inp = input("Clue (e.g. 'car 2'): ").lower().strip()
            match = re.match("(\w+)\s+(\d+)", inp)

            if match:
                clue, cnt = match.groups()
                if clue not in word_set:
                    print("I don't understand that word.")
                    continue
                return clue, int(cnt)

    def print_words(self, words: List[str], nrows: int):
        longest = max(map(len, words))
        print()
        for row in zip(*(iter(words),) * nrows):
            for word in row:
                print(word.rjust(longest), end=" ")
            print()
        print()

    def print_stats(self, my_words: set[str], opn_words: set[str],
                    neutral_words: set[str], d_words: set[str], revealing: bool):

        print("\n----------------------------------------------------------------")
        print("AGENT WORDS: %d               OPPONENT WORDS: %d" %
              (len(my_words), len(opn_words)))
        if revealing:
            print()
            print("AGENT WORDS:", my_words)
            print("OPPONENT WORDS:", opn_words)
            print("NEUTRAL WORDS:", neutral_words)
            print("DEATH WORDS:", d_words)
        print("----------------------------------------------------------------")


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
        self.wordbank = set()

    def load(self, board_bank_file, word_bank_file):
        # All words that are allowed to go onto the table

        with open(board_bank_file) as f:
            self.codenames = [line.strip() for line in f]
        with open(word_bank_file) as f:
            for line in f:
                self.wordbank.add(line.strip())


    def initialize_game(self, words):
        words_c = set(words.copy())

        agent_words = set(random.sample(list(words_c), self.cnt_agents))
        words_c.difference_update(agent_words)

        opponent_words = set(random.sample(list(words_c), self.cnt_opponents))
        words_c.difference_update(opponent_words)

        neutral_words = set(random.sample(list(words_c), self.cnt_neutral))
        words_c.difference_update(neutral_words)

        death_words = set(random.sample(list(words_c), self.cnt_death))

        used_clues = set(words)

        return agent_words, opponent_words, neutral_words, death_words, used_clues

    def play_spymaster(self, reader: Reader, strategy: Strategy):
        """
        Play a complete game, with the robot being the spymaster.
        """

        words = random.sample(self.codenames, self.cnt_rows * self.cnt_cols)
        agent_words, opponent_words, neutral_words, death_words, used_clues = self.initialize_game(
            words)

        while agent_words and opponent_words:
            reader.print_stats(agent_words, opponent_words,
                               neutral_words, death_words, revealing=True)
            reader.print_words(words, nrows=self.cnt_rows)

            clue, guesses = strategy.find_clue(
                set(words), agent_words, opponent_words, neutral_words, death_words, used_clues)
            # Save the clue, so we don't use it again
            used_clues.add(clue)

            print()
            print(
                'Clue: "{} {}"'.format(
                    clue, guesses)
            )
            print()


            reader.read_picks(words, agent_words, opponent_words,
                              neutral_words, death_words, guesses)

    def play_agent(self, reader: Reader, strategy: Strategy):
        """
        Play a complete game, with the robot being the agent.
        """

        words = random.sample(self.codenames, self.cnt_rows * self.cnt_cols)
        agent_words, opponent_words, neutral_words, death_words, used_clues = self.initialize_game(
            words)
        picked = []

        while any(w not in picked for w in agent_words):
            reader.print_stats(agent_words, opponent_words,
                               neutral_words, death_words, revealing=True)
            reader.print_words(words, nrows=self.cnt_rows)
            clue, cnt = reader.read_clue(self.wordbank)
            for _ in range(cnt):
                guess = strategy.make_guess(
                    clue, [w for w in words if w not in picked and w not in {"-O-", "-N-", "-✓-"}])
                picked.append(guess)
                print("I guess {}!".format(guess))
               
                if guess in agent_words:
                    print("\nCorrect!\n")
                    agent_words.remove(guess)
                    words[words.index(guess)] = "-✓-"
                else:
                    if guess in death_words:
                        print("\nWrong - Assassin Word x_x\n")
                        exit(0)

                    if guess in neutral_words:
                        print("\nWrong - Neutral Word :(\n")
                        neutral_words.remove(guess)
                        words[words.index(guess)] = "-N-"
                        break

                    if guess in opponent_words:
                        print("\nWrong - Opponent Word :(\n")
                        opponent_words.remove(guess)
                        words[words.index(guess)] = "-O-"
                        break


def main():
    print("...Loading codenames")
    cn = Codenames()
    cn.load(os.path.join('words', 'board_bank.txt'), os.path.join('words', 'word_bank.txt'))

    reader = TerminalReader()
    strategy = CombinedStrategy()
    print("Ready!")
    
    while True:
        try:
            mode = input("\nWill you be agent or spymaster?: ")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break

        try:
            if mode == "spymaster":
                cn.play_agent(reader, strategy)
            elif mode == "agent":
                cn.play_spymaster(reader, strategy)
        except KeyboardInterrupt:
            # Catch interrupts from play functions
            pass

if __name__ == "__main__":
    main()
