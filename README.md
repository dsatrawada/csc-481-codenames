
# Using CodeNames to Evaluate Human Perception of Inter-word Relationships
### Final Project Code Submission
#### CSC 481-01  - Knowledge Based Systems - Spring 2022 - Cal Poly
#### Professor Rodrigo Canaan 
#### Team Members: Divya Satrawada, Mansi Achuthan, Nam Nguyen, Kyle Thompson


## External Libraries/Resources
### Libraries
Our simulation requires thrid-party Python packages that can be installed using pip. These packages can be automatically collected and installed by calling `pip install -r requirements.txt` You can also install each package seperately by following these instructions:

| Package Name | Install |
| --- | --- |
|Numpy| `pip install numpy`|
|Pandas| `pip install pandas`|


### External Resources
Our project extends the pre-existing Codenames Simulation from this [Github Repository](https://github.com/thomasahle/codenames). Our modifications involved adding different gameplay scenarios and incorporating word similarities cached from Wordnet Database and Dict2Vect. We also implemented a more intuitive UI for the user to easily keep track of the game states, their scores, and other statistics. 

To pull the word similarities from Wordnet databases, we used the WordNet corpus reader from the `NLTK` library. Since we already cached all the word similarities to different `JSON` files in the `similarities` directory, installing the `NLTK` library is unnecessary to run the simulation. However, if we wish to install this library to verify the functionality of caching modules, we can do so by calling `pip install nltk`. Then, in a separate Python file, run:
```
import nltk
from nltk.corpus import wordnet as wn

nltk.download('wordnet')
```

In our project, we use a set of [400 English words](https://github.com/divyakoyy/codenames/blob/master/data/codewords.txt) to generate the game board. Then, we use a set of [10,000 Most Common English words](https://gist.github.com/deekayen/4148741) to give out clues. For making sure that our two word sets are compatible with one another, we filtered out any words in the set of 400 words that does not appear in the set of 10,000 most common English word. At the same time, we also filter out stopwords in our 10,000 word set to improve performance. 

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
In this option, one bot will make a clue, and another bot will make a guess. Same with optiob 2, the bot cannot pass to next turn like a human agent. 


## Running Validations and Collect Data
To evaulate the performance of the bot, we ran:
1. 20 games of WordNet spymaster versus Human agent 
2. 20 games of Embedding Spymaster versus Human agent
3. 30 games of Embedding Spymaster versus Wordnet agent
4. 30 games of Wordnet Spymaster versus Embedding agent
5. 20 games of Human Spymaster versus Human agent (for benchmark)


For task 1 and 2, we simply run the simulation with option 1 20 times for each bot. After each game, the simulation will output who is the winner and the total number of turns of that game. We collect those data to put in the report. The summary result is located at  **TO-DO** for task 1, and  **TO-DO** for task 2.

For task 4, we simply play games on paper and collect the result. The summary result is located at **TO-DO**

For task 2, and 3 , we **TO-DO**









