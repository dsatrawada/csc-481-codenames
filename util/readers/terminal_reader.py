
import re
from util.readers.reader import Reader

class TerminalReader(Reader):
    def read_picks(
        self, words: list[str], agent_words: set[str], opn_words: set[str],
        neutral_words: set[str], d_words: set[str],
        cnt: int
    ) -> None:
        picksCount = 0
        while True:
            guess = ""

            # Prompt to get guess pick from user
            while guess not in words or guess in {"-O-", "-N-", "-✓-"}:
                guess = input("Your guess (P to pass): ").strip()
                if guess == 'P':
                    print("\nPass...\n")
                    return

            guess_result = self.checkGuess(
                guess, words, agent_words, opn_words, neutral_words, d_words)
            if guess_result and agent_words:
                picksCount += 1
            else:
                break

            if (picksCount >= cnt):
                print("\nNo more attempts\n")
                break

    def read_clue(self, word_set) -> tuple[str, int]:
        while True:
            inp = input("Clue (e.g. 'car 2'): ").lower().strip()
            match = re.match("(\w+)\s+(\d+)", inp)

            if match:
                clue, cnt = match.groups()
                if clue not in word_set:
                    print("I don't understand that word.")
                    continue
                return clue, int(cnt)

    def print_words(self, words: list[str], nrows: int):
        longest = max(map(len, words))
        print()
        for row in zip(*(iter(words),) * nrows):
            for word in row:
                print(word.rjust(longest), end=" ")
            print()
        print()

    def print_stats(self, agent_words: set[str], opn_words: set[str],
                    neutral_words: set[str], d_words: set[str], revealing: bool):

        print("\n----------------------------------------------------------------")
        print("AGENT WORDS: %d               OPPONENT WORDS: %d" %
              (len(agent_words), len(opn_words)))
        if revealing:
            print()
            print("AGENT WORDS:", agent_words)
            print("OPPONENT WORDS:", opn_words)
            print("NEUTRAL WORDS:", neutral_words)
            print("DEATH WORDS:", d_words)
        print("----------------------------------------------------------------")

    def checkGuess(self, guess: str, words: list[str], agent_words: set[str], opn_words: set[str], neutral_words: set[str], d_words: set[str]) -> bool:
        if guess in agent_words:
            print("\nCorrect!\n")
            agent_words.remove(guess)
            words[words.index(guess)] = "-✓-"
            return True
        else:
            if guess in d_words:
                print("\nWrong - Assassin Word x_x\n")
                d_words.clear()

            elif guess in neutral_words:
                print("\nWrong - Neutral Word :(\n")
                neutral_words.remove(guess)
                words[words.index(guess)] = "-N-"

            elif guess in opn_words:
                print("\nWrong - Opponent Word :(\n")
                opn_words.remove(guess)
                words[words.index(guess)] = "-O-"

            return False
