
# Using CodeNames to Evaluate Human Perception of Inter-word Relationships
### Final Project Code Submission
#### CSC 481-01  - Knowledge Based Systems - Spring 2022 - Cal Poly
#### Professor Rodrigo Canaan 
#### Team Members: Divya Satrawada, Mansi Achuthan, Nam Nguyen, Kyle Thompson
#### [Link To Final Report](https://docs.google.com/document/d/1ift5D4DX9GdbfxECqmddA_PmytxKsOGky8njltGdmHM/edit?usp=sharing)

## External Libraries/Resources
### Libraries
Our simulation requires thrid-party Python packages that can be installed using pip. These packages can be automatically collected and installed by calling `pip install -r requirements.txt` You can also install each package seperately by following these instructions:

| Package Name | Install |
| --- | --- |
|Numpy| `pip install numpy`|
|Pandas| `pip install pandas`|
|Tqdm| `pip install tqdm`|


### External Resources
Our project extends the pre-existing Codenames Simulation from this [Github Repository](https://github.com/thomasahle/codenames). Our modifications involved adding different gameplay scenarios and incorporating word similarities cached from Wordnet Database and Dict2Vect. We also implemented a more intuitive UI for the user to easily keep track of the game states, their scores, and other statistics. 

To pull the word similarities from Wordnet databases, we used the WordNet corpus reader from the `NLTK` library. Since we already cached all the word similarities to different `JSON` files in the `similarities` directory, installing the `NLTK` library is unnecessary to run the simulation. However, if you wish to install this library to verify the functionality of caching modules, you can do so by calling `pip install nltk`. Then, in a separate Python file, run:
```
import nltk
from nltk.corpus import wordnet as wn

nltk.download('wordnet')
```

In our project, we use a set of [400 English words](https://github.com/divyakoyy/codenames/blob/master/data/codewords.txt) to generate the game board. Then, we use a set of [4000 Most Common English words](https://github.com/pkLazer/password_rank/blob/master/4000-most-common-english-words-csv.csv) to give out clues. We filter out stopwords in our 10,000 word set to improve clues. 

## Running Instruction
### Option Selection
At the main directory of our project, to start the simulation, run
```
python3 codenames_sim.py
```

The simulation should prompt different gameplay options to select:

```
----------------------------------------------------------------------------------
Codenames Simulation
----------------------------------------------------------------------------------
1. Play a game with a robot being the spymaster
2. Play a game with a robot being the agent
3. Simulate a series of gameplays where a robot being both agent and the spymaster
4. Get overall stats
5. Exit
----------------------------------------------------------------------------------
Select an option: 
```

When selecting option **1**, **2**, or **3**, we will get another prompt that ask about the type of bots we want to use. 
We  have two types of bots:
1. **Embedding**: The bot will use Embedding Dict2Vect word similarities to either find clues, or make guesses, or both
2. **WordNet**:  The bot will use word similarities from Wordnet Database to either find clues, or make guesses, or both. Word similarities from Wordnet Database based on three semantic relationship (Hypernym-Hyponym, Meronym-Holonym, and Antonym)

```
----------------------------------------------------------------------------------
Codenames Simulation
----------------------------------------------------------------------------------
1. Play a game with a robot being the spymaster
2. Play a game with a robot being the agent
3. Simulate a series of gameplays where a robot being both agent and the spymaster
4. Get overall stats
5. Exit
----------------------------------------------------------------------------------
Select an option: 1
Possibilities:
1. Embedding
2. WordNet
Which bot will be SpyMaster?: 2
```
When selecting option **4**, the simualtion program will print out 
1. Total wins from beginning of the session
2. Total loses from beginning
3. Average number of turn per each game

### Gameplay 
#### Option 1.  Play a game with a robot being the spymaster
In this option, after the bot provides a clue, we can start type in our guesses. The number of availabe attempts equals to the number of words associated with a clue. If we guess corectly, and we still have unused attempts, we may either make another guess, or pass to a new turn. If we guess incorectly in any neutral words or  opponent words, we will move to a new turn where the bot give you another clue. 

```
----------------------------------------------------------------
AGENT WORDS: 9               OPPONENT WORDS: 8
----------------------------------------------------------------

   change     ivory       fan   beijing     eagle 
      bed horseshoe   germany    strike    school 
   bridge      foot       tap      wake    spring 
     head      mass   disease      mail     cover 
     time    berlin     mount telescope    button 

Thinking...

Clue: "sleep 1"

Your guess (P to pass):
```
The game ends when we either 
1. Have no more agent words to guess (Winning)
2. Have no more opponent words to guess (Losing) 
3. Guess an  assasin word (Losing) 

When the game ends, the simulation will print the final verdict, and how many turns we have used.

#### Option 2 - Play a game with a robot being the agent
In this option, after the we provide a clue at each turn, the bot will attempt to guess the correct words. Notice that the bot *cannot* pass to the next turn, like a human player.
```
----------------------------------------------------------------
AGENT WORDS: 9               OPPONENT WORDS: 8

AGENT WORDS: {'band', 'fly', 'flute', 'germany', 'pie', 'part', 'millionaire', 'duck', 'capital'}
OPPONENT WORDS: {'australia', 'czech', 'lawyer', 'casino', 'grace', 'drop', 'apple', 'luck'}
NEUTRAL WORDS: {'triangle', 'forest', 'foot', 'slug', 'rome', 'olympus', 'back'}
DEATH WORDS: {'bomb'}
----------------------------------------------------------------

    olympus millionaire        band     germany       grace
      apple      forest        luck        rome         pie
    capital         fly    triangle        back        part
       bomb      casino        slug   australia       czech
       duck      lawyer        foot        drop       flute

Clue (e.g. 'car 2'): money 2
I guess part!

Correct!

I guess capital!

Correct!
```

#### Option 3 -  Simulate a series of gameplays where a robot being both agent and the spymaster
In this option, one bot will make a clue, and another bot will make a guess. Same with optiob 2, the bot cannot pass to next turn like a human agent. We use this option mainly for evaluation. For this reason, we have a setting that allows us to tune our main hyperparameter, sigma. The simulator plays games at each value for sigma for the specified number of iterations. This setting is only configurable by editing the source code by editing the `try_sigma` list in the `play_sim` function of `codenames_sim.py`. Running a simulation will automatically save results to the results/sim_results directory. We produce plots for these results by running the file results.py in the util directory. Specifically, navigate to the util directory and run `python3 results.py`. These results take some time to produce. The results of our previous simulations are in the [results](https://github.com/dsatrawada/csc-481-codenames/tree/main/results) folder. 
```
...Loading codenames
Ready!
----------------------------------------------------------------------------------
Codenames Simulation
----------------------------------------------------------------------------------
1. Play a game with a robot being the spymaster
2. Play a game with a robot being the agent
3. Simulate a series of gameplays where a robot being both agent and the spymaster
4. Get overall stats
5. Exit
----------------------------------------------------------------------------------
Select an option: 3
Possibilities:
1. Embedding
2. WordNet
Who will be SpyMaster?: 1
Who will be Agent?: 2
Select number of iterations: 15
Automatically prints overall stats and exits the program when all the gameplays are done (Y/N): Y
TRYING SIGMA:  22
ITERATION: 0
```

You can see that the user has some flexibility when running the agent pair simulations. The user can select the type of agent that will be the spymaster, and the type of agent that will be the guesser (agent in the UI). The user can also specify the number of iterations to run for each value of sigma. A file will be written to the results directory for each value of sigma (specified in codenames.py). 

We ran a twin trial for both the Wordnet and Embedding spymaster, but these results were overwritten in one of our merges. We also lost some functionality that plots the results in the merge. However, the results are given in the report that accompanies this repository. They can be reproduced by setting the spymaster and guesser to be the same agent in the simulation. The Embedding spymaster should win some if not all of its games, and the Wordnet Spymaster should win just about half of its games.


## Principle Results
To evaulate the performance of the bot, we ran:
1. 225 games of Embedding spymaster and Wordnet guesser. 
2. 225 games of Wordnet spymaster and Embedding guesser.
3. 15 games of Embedding spymmaster and Embedding guesser (Not in repository ~15 min runtime).
4. 15 games of Wordnet Spymaster versus Wordnet guesser (Not in repository ~30 min runtime).
5. 10 games of Embedding spymaster and human guesser. (Not in repository)
6. 10 games of Wordnet spymaster and human guesser. (Not in repository)
7. 10 games of Human spymaster and human guesser. (Not in Repository)
8. 20 games of Human Spymaster versus Human agent (for benchmark)

### Conclusions
- Embedding spymaster and Wordnet guesser is worse than Wordnet Spymaster and Embedding Guesser.
- Embedding twins win every or almost every time, and Wordnet twins win about half of the time.
- Humans playing with humans are better than hummans guessing for agent spymasters.
- Wordnet spymasters and Embedding spymasters produced similar results to eachother, but it is more fun to play against embedding spymasters. 
