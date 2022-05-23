from typing import Iterable
import numpy as np

class LossNode:
    def __init__(
            self, 
            node_id = "",
            exp_other = 0, # All non-agent cards are leaf nodes so we can combine them
            exp_a = 0, # Expected score for agent words if it is the last turn
            children = [],
            prob_children = []
            ):
        self.exp_other = exp_other
        self.exp_a = exp_a
        self.children = children
        self.prob_children = prob_children
        self.id = node_id


memoized_nodes = {} # Global variable to memoize the loss nodes
memoized_scores = {} # Global valriable to memoize scores of the loss tree
def loss(max_words: int, a_sim: Iterable[float], o_sim: Iterable[float], 
        n_sim: Iterable[float], l_sim: float, prob_func) -> Iterable[float]:
    """
    Given similarities between a word and a board, return a list of expected
    change in cards given that the guess applies to 1, 2, ... max_words cards
    :param max_words: number of words a hint applies to. The depth of the 
        simulation tree will then be min(max_words + 1, len(a_sim))
    :param a_sim: list of similarities between the guess, and each agent word
    :param o_sim: list of similarities between the guess, and each oponent word
    :param n_sim: list of similarities between the guess, and each neutral word
    :param l_sim: similarity between the guess and the assasin word
    :param prob_func: how to get the probability score for a single word given
        the similarity between the word and the guess. This score will be divided
        by the sum of all the scores on the board to get a value between 0 and 1
    """
    global memoized_nodes, memoized_scores
    memoized_nodes = {}

    max_depth = min(max_words + 1, len(a_sim))

    a_sim_np = np.array(a_sim)
    o_sim_np = np.array(o_sim)
    n_sim_np = np.array(n_sim)
    l_sim_np = np.array([l_sim])

    o_sim_scores = np.full(len(o_sim_np), -1)
    n_sim_scores = np.full(len(n_sim_np), 0)
    l_sim_scores = np.full(len(l_sim_np), -1 * (len(o_sim_np) + 1))

    other_sim = np.concatenate([o_sim_np, n_sim_np, l_sim_np])
    other_scores = np.concatenate([o_sim_scores, n_sim_scores, l_sim_scores])
    prob_other = prob_func(other_sim)
    sum_prob_other = prob_other.sum()

    a_ids = ["w" + "{:03d}".format(i) for i in range(len(a_sim))]

    loss_tree = build_loss_tree(max_depth, a_sim_np, a_ids, 0, prob_other,
            sum_prob_other, other_scores, prob_func)

    scores = []
    for i in range(1, max_depth + 1):
        memoized_scores = {}
        scores.append(get_scores(loss_tree, i))
    return scores
        


def build_loss_tree(max_depth: int, a_sim: np.ndarray, a_id: list[str], depth: int, 
        prob_other: np.ndarray, sum_prob_other: float, score_other: np.ndarray, 
        prob_func) -> LossNode:
    """
    Recursive function to construct the loss tree that will be used
    to calculate the loss for the guess. Memoize each distinct combination
    :param max_depth: maximum number of guesses allowed 
    :param a_id: list of names for the agent words to use as identifiers
    :param a_sim: list of similarities between the guess, and each agent word
    :param depth: number of positive words guessed so far in the tree
    :param prob_other: all non_agent probabilities
    :param sum_prob_other: sum of non_agent probabilities
    :param score_other: change in cards of non_agent cards
    :param prob_func: how to get the probability score for a single word given
        the similarity between the word and the guess. This score will be divided
        by the sum of all the scores on the board to get a value between 0 and 1
    """
    global memoized_nodes
    sorted_id = ''.join(sorted(a_id))
    if sorted_id in memoized_nodes:
        return memoized_nodes[sorted_id]
    
    prob_a = prob_func(a_sim)
    sum_all = prob_a.sum() + sum_prob_other
    prob_others = prob_other / sum_all
    val_others = score_other + depth
    val_a = np.full(len(a_sim), depth + 1)
    prob_a = prob_a / sum_all

    ret_node = LossNode(
            node_id=sorted_id,
            exp_other=val_others @ prob_others,
            exp_a = val_a @ prob_a,
            children = [],
            prob_children = [],
            ) #eother, children, pchildren

    if max_depth <= 1:
        return ret_node

    # Create child nodes
    for i in range(len(a_sim)):
        a_sim_new = np.concatenate([a_sim[:i], a_sim[i+1:]])
        a_id_new = a_id.copy()
        a_id_new.remove(a_id[i])
        ret_node.children.append(
                build_loss_tree(max_depth - 1, a_sim_new, a_id_new, depth + 1,
                    prob_other, sum_prob_other, score_other, prob_func))
    ret_node.prob_children = prob_a

    memoized_nodes[sorted_id] = ret_node
    return ret_node


def get_scores(loss_tree: LossNode, max_depth: int) -> float:
    """
    Traverses a loss tree to calculate the score of the tree
    for some maximum depth
    """
    global memoized_scores
    if loss_tree.id in memoized_scores:
        return memoized_scores[loss_tree.id]

    score = loss_tree.exp_other
    if max_depth == 0:
        return 0
    if max_depth == 1:
        score += loss_tree.exp_a
        memoized_scores[loss_tree.id] = score
        return score

    for i in range(len(loss_tree.children)):
        score += loss_tree.prob_children[i] * \
                get_scores(loss_tree.children[i], max_depth - 1)

    memoized_scores[loss_tree.id] = score
    return score


def print_tree(loss_tree: LossNode) -> None:
    """
    Prints the given loss tree for debugging
    :param loss_tree: the tree to print
    """
    print(loss_tree.id)
    for child in loss_tree.children:
        print_tree(child)



if __name__ == '__main__':
    print(loss(
            max_words=4, 
            a_sim=[0.1, 1, 0.1, 0.3, 0.3, 0.4, 0.8, 0.1, 1], 
            o_sim=[0.1, 0.2, 0.3, 0.4, 0.1, 0.1, 0.3], 
            n_sim=[0.1, 0.1, 0.1, 0.3, 0.4, 0.8, 0.4], 
            l_sim=0.2, 
            prob_func=lambda x: x))
    
