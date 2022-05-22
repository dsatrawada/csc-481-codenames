import sys
import re 
import nltk
from nltk.corpus import wordnet as wn
nltk.download('wordnet')
nltk.download('omw-1.4')

def filter_words(filename):
    '''
    Filters all words in the file to only words in wordnet
    and writes them back to the file
    '''
    with open(filename, 'r') as fin:
        lines = fin.readlines()
    words = []
    for line in lines:
        tokens = line.split() 
        if len(tokens) != 1: 
            continue
        words.append(tokens[0].strip().lower())

    wn_words = [w for w in words if len(wn.synsets(w)) > 0] 

    with open(filename, 'w') as fout:
        fout.write('\n'.join(wn_words))
     

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Please provide the file to filter")
        print("filter.py <file>")
        exit()
    filter_words(sys.argv[1])


