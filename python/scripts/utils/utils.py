#!/usr/bin/env python
#!/usr/bin/python3

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

    list_a = ['a','b','c']
    list_b = ['a','b','d']
    results = diff_lists(list_a, list_b, verbose=in_verbose)
    print(results)