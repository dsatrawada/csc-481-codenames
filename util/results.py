import sys, os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np




RESULT_DIR = os.path.join('..', 'results', 'sim_results')
PLOT_DIR = os.path.join('..', 'results', 'plot_results')


def parse_name(filename):
    '''
    Parse the file name created by the simulation. 
    Only has to handle the part of the filename
    before the extention
    '''
    no_ext = filename.split(';')
    spy = no_ext[0]
    spy_toks = spy.split('_')
    spy_name = spy_toks[0]
    spy_sig = spy_toks[1]
    ag = no_ext[1]

    return spy_name, int(spy_sig), ag

def get_score(row):
    '''
    Get the score of a codenames game given
    a row in teh statistics dataframe
    '''
    if row['Result'] == 'win':
        return 24 - row['Num Turns']
    return row['Num Turns'] - 24


def create_plots():
    '''
    Plots the results found in results/sim_results
        - For any given game we can produce a score based
          on the number of turns and the result if we say:
            - Losing in more turns is better than losing
              in less turns.
            - Winning in less turns is better than winning
              in more turns.
            - The maximimum number of turns in a loss is 23 and
              the maximum number of turns in a win is 23. Scores
              (Higher is better) will be calculated by 
              - 24 - w if win
              - 2 - 24 if loss
    '''
    if not os.path.exists(RESULT_DIR):
        os.makedirs(RESULT_DIR)
    if not os.path.exists(PLOT_DIR):
        os.makedirs(PLOT_DIR)

    res_tups = []
    for f in os.listdir(RESULT_DIR):
        ext = f.split('.')
        if len(ext) < 2 or ext[1] != 'csv':
            continue            
        spy_name, spy_sig, ag = parse_name(ext[0])
        f_df = pd.read_csv(os.path.join(RESULT_DIR, f))
        f_df['Score'] = f_df.apply(get_score, axis=1)
        res_tups.append((spy_name, spy_sig, f_df['Score'].mean()))

    res_df = pd.DataFrame(res_tups, columns=['Spymaster', 'Sigma', 'Score'])
    fig, ax = plt.subplots()
    for name, df in res_df.groupby('Spymaster'):
        plot_df = df.sort_values('Sigma')
        ax.plot(plot_df['Sigma'], plot_df['Score'], label=name + ' Spymaster')
    ax.set_xlabel('Value for Sigma')
    ax.set_ylabel('Score')
    ax.set_title('Performance of Agents\nWith Various Values of Sigma', loc='left')
    fig.legend()
    plt.savefig(os.path.join(PLOT_DIR, 'Simulation Results'))


if __name__ == '__main__':
    create_plots()
