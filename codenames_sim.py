import os
import random
from typing import List, Tuple
import re
from util.readers.reader import Reader
from util.readers.terminal_reader import TerminalReader
from util.strategies.strategy import Strategy
from util.strategies.combined_strategy import CombinedStrategy
import pandas as pd

class Codenames:
    def __init__(self, reader: Reader, cnt_rows=5, cnt_cols=5, cnt_agents=9, cnt_opponents=8, cnt_neutral=7, cnt_death=1):
        """
        :param cnt_rows: Number of rows to show.
        :param cnt_cols: Number of columns to show.
        :param cnt_agents: Number of agent (player) words.
        :param cnt_opponents: Number of opponent words.
        :param cnt_neutral: Number of neutral words.
        :param cnt_death: Number of assasin words.
        """
        self.cnt_rows = cnt_rows
        self.cnt_cols = cnt_cols
        self.cnt_agents = cnt_agents
        self.cnt_opponents = cnt_opponents
        self.cnt_neutral = cnt_neutral
        self.cnt_death = cnt_death

        # Local variables to keep track of stats
        self.reader = reader
        self.win = 0
        self.lose = 0
        self.tie = 0
        self.turn_records = []

        self.boardbank = []
        self.wordbank = set()

        # Path for results
        self.result_path = os.path.join('results', 'sim_results')

    def load(self, board_bank_file, word_bank_file):
        """
        Load the boardbank and the wordbank. Boardbank is a set of 
        words that the game board will draw from, while wordbank
        is a set of common English wordd that we can use to give clues
        :param board_bank_file: path to the boardbank file
        :param agent_words: path to the wordbank file
        """

        with open(board_bank_file) as f:
            self.boardbank = [line.strip() for line in f]
        with open(word_bank_file) as f:
            for line in f:
                self.wordbank.add(line.strip())

    def printGameStats(self):
        """
        Prints the stats of the current codenames session, including:
            1. Total wins from beginning
            2. Total loses from beginning
            3. Avg number of turn per each game
        """

        print("\nOverall Stats")
        print(" - Total wins from beginning:", self.win)
        print(" - Total loses from beginning:", self.lose)
        print(" - Total ties from beginning:", self.tie)
        print(" - Avg number of turn per each game:",
              sum(self.turn_records) / len(self.turn_records), "\n")

    def get_game_result(self, agent_words: set[str], opponent_words: set[str], death_words: set[str]):
        """
        Gets the final verdict of the game, including who wins, and the the number of turn of that game,
        then update the stats.
        :param agent_words: set of remaining correct words
        :param opn_words: set of remaining opponent words
        :param d_words: set of remaining assasin (death) words
        """
        ret_val = ''
        if (not agent_words and opponent_words and death_words):
            print("\nYou win!")
            self.win += 1
            ret_val = 'win'
        elif (agent_words and (not opponent_words or not death_words)):
            print("\nYou lose!")
            self.lose += 1
            ret_val = 'lose'
        else:
            print("\nTie!")
            self.tie += 1
            ret_val = 'tie'
        print("Number of the turn of this game:",
                self.turn_records[len(self.turn_records) - 1])
        return ret_val

    def reveal_codenames(self, agent_words, opponent_words, neutral_words, death_words):
        print("Revealing remaining codenames...\n")
        print("Agent Words: ", agent_words)
        print("Opponent Words: ", opponent_words)
        print("Neutral Words: ", neutral_words)
        print("Death Words: ", death_words)

    def initialize_game(self, words):
        """
        Generate the Codenames board at the beginning of the game 
        :param words: a set of words that the game board will draw from
        :return (set of agent words, set of opponent words, set of neutral words, set of death words, set of words that cannot be used as clues)
        """
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

    def play_spymaster(self, strategy: Strategy):
        """
        Play a complete game, with the robot being the spymaster.
        :param reader: a Reader object from the Reader class
        :param strategy: a Strategy object forom the Strategy class
        """

        words = random.sample(self.boardbank, self.cnt_rows * self.cnt_cols)
        agent_words, opponent_words, neutral_words, death_words, used_clues = self.initialize_game(
            words)
        turn = 0

        while agent_words and opponent_words and death_words:
            turn += 1
            self.reader.print_stats(agent_words, opponent_words,
                               neutral_words, death_words, revealing=False)
            self.reader.print_words(words, nrows=self.cnt_rows)

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

            self.reader.read_picks(words, agent_words, opponent_words,
                              neutral_words, death_words, guesses)

        # Game is ended. Determine the winner
        self.turn_records.append(turn)
        self.get_game_result(agent_words, opponent_words, death_words)

    def play_agent(self, strategy: Strategy):
        """
        Play a complete game, with the robot being the agent.
        :param reader: a Reader object from the Reader class
        :param strategy: a Strategy object forom the Strategy class
        """

        words = random.sample(self.boardbank, self.cnt_rows * self.cnt_cols)
        agent_words, opponent_words, neutral_words, death_words, used_clues = self.initialize_game(
            words)
        turn = 0
        while agent_words and opponent_words and death_words:
            turn += 1
            self.reader.print_stats(agent_words, opponent_words,
                               neutral_words, death_words, revealing=True)
            self.reader.print_words(words, nrows=self.cnt_rows)
            clue, cnt = self.reader.read_clue(self.wordbank)
            for _ in range(cnt):
                guess = strategy.make_guess(
                    clue, [w for w in words if w not in {"-O-", "-N-", "-???-"}])

                print("I guess {}!".format(guess))

                game_result = self.reader.checkGuess(
                    guess, words, agent_words, opponent_words, neutral_words, death_words)
                if not game_result or not agent_words:
                    break

        # Game is ended. Determine the winner
        self.turn_records.append(turn)
        self.get_game_result(agent_words, opponent_words, death_words)
        self.reveal_codenames(agent_words, opponent_words,
                              neutral_words, death_words)

    def play_sim(self, sm_strategy: Strategy, ag_strategy: Strategy, 
            num_sim: int, auto_exit: bool): 
        """
        Play a complete game, with the robot being both the agent and the spymaster.
        :param reader: a Reader object from the Reader class
        :param sm_strategy: Strategy for the spymaster to use
        :param ag_strategy: Strategy for the agent to use
        :param num_sim: number of gameplays to perform
        :param auto_exit: an option to automatically print out the overall stats and exit the program when all the gameplays are done
        """

        try_sigma = [22, 24, 26, 28, 30] 
        for sig in try_sigma:
            sm_strategy.sigma = sig
            if os.path.exists(os.path.join(self.result_path, sm_strategy.get_id() + '|' + ag_strategy.name + '.csv')):
                continue
            stats =  []  
            for i in range(num_sim):
                print('TRYING SIGMA: ', sig)
                print('ITERATION:', i)
                # Initlize a game
                words = random.sample(self.boardbank, self.cnt_rows * self.cnt_cols)
                agent_words, opponent_words, neutral_words, death_words, used_clues = self.initialize_game(
                    words)
                turn = 0

                while agent_words and opponent_words and death_words:
                    turn += 1
                    self.reader.print_stats(agent_words, opponent_words,
                                    neutral_words, death_words, revealing=True)
                    self.reader.print_words(words, nrows=self.cnt_rows)
                    clue, cnt = sm_strategy.find_clue(
                        set(words), agent_words, opponent_words, neutral_words, death_words, used_clues)
                    used_clues.add(clue)
                    print()
                    print(
                    'Clue: "{} {}"'.format(
                        clue, cnt)
                    )
                    print()

                    for _ in range(cnt):
                        guess = ag_strategy.make_guess(
                            clue, [w for w in words if w not in  {"-O-", "-N-", "-???-"}])
                    
                        print("I guess {}!".format(guess))
                        game_result = self.reader.checkGuess(guess, words, agent_words, opponent_words, neutral_words, death_words)
                        if not game_result or not  agent_words:
                            break
                        
                # Game is ended. Determine the winner
                self.turn_records.append(turn)
                result = self.get_game_result(agent_words, opponent_words, death_words)
                stats.append((i, result, turn))

            
            res_df = pd.DataFrame(stats, columns=['Iteration', 'Result', 'Num Turns'])
            res_df.to_csv(os.path.join(self.result_path, sm_strategy.get_id() + '|' + ag_strategy.name + '.csv'), index=False)
            
        if (auto_exit):
            self.printGameStats()
            exit(0)


def main():
    print("...Loading codenames")
    cn = Codenames(reader= TerminalReader())
    cn.load(os.path.join('words', 'board_bank.txt'),
            os.path.join('words', 'word_bank.txt'))

    print("Ready!")

    while True:
        option = 0
        print("----------------------------------------------------------------------------------")
        print("Codenames Simulation")
        print("----------------------------------------------------------------------------------")
        print("1. Play a game with a robot being the spymaster")
        print("2. Play a game with a robot being the agent")
        print("3. Simulate a series of gameplays where a robot being both agent and the spymaster")
        print("4. Get overall stats")
        print("5. Exit")
        print("----------------------------------------------------------------------------------")

        while option < 1 or option > 5:
            value = input("Select an option: ")
            option = int(value.strip())

        if option == 1:
            print('Possibilities:')
            print('1. Embedding')
            print('2. WordNet')
            spy_opt = ""
            while spy_opt not in set(['Embedding', 'WordNet', '1', '2']):
                spy_opt = input('Which bot will be SpyMaster?: ').strip()
            if spy_opt == 'WordNet' or spy_opt == '2':
                spym = CombinedStrategy()
            else:
                spym = Strategy('d2v_sim.json')
            
            cn.play_spymaster(spym)

        elif option == 2:
            print('Possibilities:')
            print('1. Embedding')
            print('2. WordNet')
           
            ag_opt = ""
            while ag_opt not in set(['Embedding', 'WordNet', '1', '2']):
                ag_opt = input('Which bot will be Agent?: ').strip()
            
            if ag_opt == 'WordNet' or ag_opt == '2':
                ag = CombinedStrategy()
            else:
                ag = Strategy('d2v_sim.json')

            cn.play_agent(ag)  
        elif option == 3:
            print('Possibilities:')
            print('1. Embedding')
            print('2. WordNet')

            spy_opt = ""
            while spy_opt not in set(['Embedding', 'WordNet', '1', '2']):
                spy_opt = input('Who will be SpyMaster?: ')
            ag_opt = ""
            while ag_opt not in set(['Embedding', 'WordNet', '1', '2']):
                ag_opt = input('Who will be Agent?: ')

            if spy_opt == 'WordNet' or spy_opt == '2':
                spym = CombinedStrategy()
            else:
                spym = Strategy('d2v_sim.json')

            if ag_opt == 'WordNet' or ag_opt == '2':
                ag = CombinedStrategy()
            else:
                ag = Strategy('d2v_sim.json')

            value = input("Select number of iterations: ")
            num_iter = int(value.strip())
            value = input(
                "Automatically prints overall stats and exits the program when all the gameplays are done (Y/N): ")
            auto_exit = True if value.strip() == 'Y' else False
            cn.play_sim(spym, ag, num_iter, auto_exit)
        elif option == 4:
            cn.printGameStats()
        else:
            print("Exited with code 0")
            exit(0)


if __name__ == "__main__":
    main()
