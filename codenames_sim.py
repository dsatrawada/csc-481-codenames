import os
import random
from typing import List, Tuple
import re
from strategy import Strategy
from hypernym_strategy import HypernymStrategy
from combined_strategy import CombinedStrategy
from reader import Reader
from terminal_reader import TerminalReader

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

        with open(word_bank_file) as f:
            self.codenames = [line.strip() for line in f]

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
                               neutral_words, death_words, debug=True)
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
                               neutral_words, death_words, debug=True)
            reader.print_words(words, nrows=self.cnt_rows)
            print("Your words:", ", ".join(
                w for w in agent_words if w not in picked))
            # TODO: change word bank for clues?
            clue, cnt = reader.read_clue(self.codenames)
            for _ in range(cnt + 1):
                guess = self.make_guess(
                    clue, [w for w in words if w not in picked])
                picked.append(guess)
                print("I guess {}!".format(guess))
                if guess not in agent_words or guess in picked:
                    print("I got it wrong. Sorry about that!")
                    break
            else:
                print("I got them all!")


def main():
    print("...Loading codenames")
    cn = Codenames()
    cn.load(os.path.join('words', 'board_bank.txt'))
    reader = TerminalReader()
    strategy = CombinedStrategy(0,0, 0, 0)
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