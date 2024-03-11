#!/usr/bin/env python
#!/usr/bin/python3

from typing import Literal

def diff_lists(list_a:list, list_b:list, verbose:bool=False):
    """
    Return list of items in list_a which are not in list_b.
    """
    s1 = set(list_a)
    s2 = set(list_b)
    results = list(s1-s2)
    if verbose:
        print(f"set one length: {len(s1)}")
        print(f"set two length: {len(s2)}")
        print(f"differences of sets length: {len(s2)}")
    return results

def sort_dict(data:dict, sort_by:Literal['key', 'value']='key')->dict:
    """
    src: https://www.geeksforgeeks.org/python-sort-python-dictionaries-by-key-or-value/
    """
    # TODO: implement ability to sort by either key OR values.
    sorted_key_list = list(data.keys())
    sorted_key_list.sort()
    sorted_dict = { i: data[i] for i in sorted_key_list }
    return sorted_dict

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-v','--verbose',
        dest='verbose',
        action='store_true',
        default=False,
        help=f'Enable verbose mode.')
    parser.add_argument('-i', '--input',
                        dest='input',
                        action='store',
                        type=str)
    args = parser.parse_args()
    in_verbose = bool(args.verbose is True)

    results = None
    if args.input == 'diff_lists':
        list_a = ['a','b','c']
        list_b = ['a','b','d']
        results = diff_lists(list_a, list_b, verbose=in_verbose)    # contents in list_a which are not in list_b
    else:
        data = { "3": "three", "1": "one", "2": "two" }
        results = sort_dict(data)

    print(f"data: {data}\n")
    print(f"results: \n{results}\n")