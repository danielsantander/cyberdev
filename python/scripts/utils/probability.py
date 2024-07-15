#!/usr/bin/env python
#!/usr/bin/python3


"""
P(A) = n(A)/n(S)

Where:
- P(A) is the probability of an event “A”
- n(A) is the number of favorable outcomes (Here, the favorable outcome means the outcome of interest.)
- n(S) is the total number of events in the sample space
"""

import argparse
import logging
import sys

DEBUG_MODE = False

# probability of event A = num of favorable outcomes / number of total outcomes -> P(A) = n(A)/n(S)
probability = lambda a,s: (a/s)#*100

def factorial(n:int):
    """
        Time Complexity: O(n)
    """
    fact = 1
    for i in range(1, n+1):
        fact = fact * i
    return fact

def probability_of_event(num_of_favorable_outcomes:int, num_total_outcomes:int, return_percentage:bool=True, round_placement:int=2)->float:
    results:float = probability(num_of_favorable_outcomes, num_total_outcomes)
    return round((results*100), round_placement) if return_percentage else results

def conditional_probability(a_b:float, b:float)->float:
    """
        Conditional Probability of A given B	P (A|B) = P(A ∩ B)⁄P(B)
        Conditional Probability of B given A	P (B|A) = P(B ∩ A)⁄P(A)

        CAUTION: In general P( A | B) is not equal to P( B | A). That is the probability of A given the event B is not the same as the probability of B given the event A.
    """
    probability_of_a_given_b = a_b / b
    return probability_of_a_given_b


# -----------------------------
# PERMUTATIONS & COMBINATIONS
# -----------------------------
def calculate_combination(num_items_in_set:int, num_items_selected_from_set:int):
    """
        Combinations are groups where order does not matter.
        FORMULA: c_n_k = n!/(n-k)!k!
        c_n_k =	number of combinations
        n     = total number of objects in the set
        k     = number of choosing objects from the set
    """
    n_min_k = num_items_in_set - num_items_selected_from_set
    results = (factorial(num_items_in_set)) / ((factorial(num_items_selected_from_set))*(factorial(n_min_k)))
    return results

def calculate_permutation(num_items_in_set:int, num_items_selected_from_set:int):
    """
    Permutations are lists where order matters.
    FORMULA: p_n_k = n!/(n-k)!
        p_n_k =	number of permutations
        n     = total number of objects in the set
        k     = number of choosing objects from the set
    """
    n_min_k = num_items_in_set - num_items_selected_from_set
    results = (factorial(num_items_in_set)) / (factorial(n_min_k))
    return results

def permutations(string:str, step:int=0):
    """
    source: https://www.tutorialspoint.com/How-to-find-all-possible-permutations-of-a-given-string-in-Python#:~:text=To%20find%20all%20possible%20permutations%20of%20a%20given%20string%2C%20you,in%20the%20iterable%20as%20tuples.
    """
    if step == len(string):
        # finished, print permutation
        print("".join(string))
    for i in range(step, len(string)):

        # copy string (store as array)
        string_copy = [c for c in string]

        # swap the current index with the step
        string_copy[step], string_copy[i] = string_copy[i], string_copy[step]

        # recurse on the portion of the string that has not been swapped yet
        permutations(string_copy, step + 1)
        # permutations("".join(string_copy), step + 1)
        # permutations(string, step + 1)

# -----------------------------

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # list of actions to use
    cat_list = ['combination', 'permutation', 'cards']
    parser.add_argument('category',
            choices=cat_list,
            metavar=f'category: {cat_list}',
            action='store',
            type=str,
            help='Category of probabilities to calculate.')
    args = parser.parse_args()
    category = str(args.category)
    results = None

    if category in ['combination', 'permutation']:
        num_items_in_set = int(input('Enter total number of items in set: ') or 0)
        num_items_selected = int(input('Enter number of items to select: ') or 0)
        print(f"num_items_in_set: {num_items_in_set}")
        print(f"num_items_selected: {num_items_selected}")
        if num_items_in_set and num_items_selected:
            results = calculate_combination(num_items_in_set, num_items_selected) if category == 'combination' else calculate_permutation(num_items_in_set, num_items_selected)
            print(f"{category.upper()}:\nFor number items in the set ({num_items_in_set}) and number of items selected ({num_items_selected}), the {category.lower()} is: {results}")

        else:
            print("HAVE NO DATA")
        sys.exit()

    if category == 'cards':
        num_cards_in_pack = 52

        # Probability of selecting an ace from a deck
        # P(Ace) = (Number of favorable outcomes) / (Total Number of Favorable Outcomes)
        # P(Ace) = 4/52 = 1/13
        num_aces = 4
        num_fav_outcomes = 4
        results = probability_of_event(num_aces, num_cards_in_pack, True)
        results = str(results) + "%"
        print (f'\nProbability of selecting an ace from a deck: {results}')

    print ("\n")
    sys.exit()
