from util.readers.reader import Reader
from typing import List, Tuple
import re


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

            if (picksCount > cnt):
                print("\nNo more attempts\n")
                break

    def read_clue(self, word_set) -> Tuple[str, int]:
        while True:
            inp = input("Clue (e.g. 'car 2'): ").lower()
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
                    neutral_words: set[str], d_words: set[str], debug: bool):

        print("\n----------------------------------------------------------------")
        print("AGENT WORDS: %d               OPPONENT WORDS: %d" %
              (len(my_words), len(opn_words)))
        if debug:
            print("\nDebugInfo:")
            print("     AGENT WORDS:", my_words)
            print("     OPPONENT WORDS:", opn_words)
            print("     NEUTRAL WORDS:", neutral_words)
            print("     DEATH WORDS:", d_words)
        print("---------------------------------------------------------------")
