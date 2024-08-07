#!/usr/bin/env python
#!/usr/bin/python3

"""
Random cool python tricks that live in the void.

"""

import json
import random
import sys
import time
from datetime import datetime
from typing import Union


def afk():
    import pyautogui as pag
    # note: may need to upgrade numpy -> python3 -m pip install --upgrade numpy
    try:
        while True:
            x = random.randint(600,700)
            y = random.randint(200,600)
            print (f"moving to {x},{y} ...")
            pag.moveTo(x,y,0.5)
            time.sleep(2)
    except KeyboardInterrupt:
        print("Exiting...")
        sys.exit()

def dictionary_comprehension(data:list[dict], key:str):
    results = { entry[key]:entry for entry in data }
    return results

def remove_dupes_from_list(data:list[Union[str,int]]):
    """
    Remove duplicates from list while maintaining order of list.

    - dict.fromkeys() to remove dupes and maintain order (dictionary keys must be unique).
    - return dictionary keys as list.
    """
    # return dict.fromkeys(data)  # {'a': None, 'b': None, 'c': None}
    return list(dict.fromkeys(data).keys()) # ['a', 'b', 'c']

# Immediately Invoked Function Expression (IIFE):
# Runs immediately as code is encountered, as result it cannot be run again.
# It uses a lambda with an underscore that calls the function immediately.
# Can be used as a variable -> print(start_time) -> 13:19:38
@lambda _: _()
def start_time() -> str:
    """ Return current date formatted so it only returns time back. """
    date = datetime.now()
    return f"{date:%T}"

if __name__ == '__main__':
    import argparse
    list_of_choices = [
        'afk',
        'dictionary_comprehension',
        'remove_dupes_from_list',
        'start_time'
    ]
    parser = argparse.ArgumentParser()
    parser.add_argument('action',
        choices=list_of_choices,
        action='store',
        type=str,
        help='Action to perform.')
    parser.add_argument('--data',
        dest="data",
        action="store",
        type=str,
        help="Data to processes.")
    args = parser.parse_args()
    # if args.action in ['remove_dupes_from_list'] and not args.data:
    #     parser.error(f'The \'{args.action}\' action requires data input.')

    if args.action == 'dictionary_comprehension':
        # test dictionary comprehension
        accts_list: list[dict] = [ {"account_name": "test_01", "account_id": 1, "is_enabled": True},
                                {"account_name": "test_02", "account_id": 2, "is_enabled": False},
                                {"account_name": "test_03", "account_id": 3, "is_enabled": True} ]
        print (f"\naccts_list before:\n{accts_list}")
        accts_by_name = dictionary_comprehension(accts_list, "account_name")
        print ("\naccts_list after:\n" + json.dumps(accts_by_name, indent=2))
        # OUTPUT
        # {
        #     "test_01": {
        #         "account_name": "test_01",
        #         "account_id": 1,
        #         "is_enabled": true
        #     },
        #     "test_02": {
        #         "account_name": "test_02",
        #         "account_id": 2,
        #         "is_enabled": false
        #     },
        #     "test_03": {
        #         "account_name": "test_03",
        #         "account_id": 3,
        #         "is_enabled": true
        #     }
        # }

    if args.action == 'remove_dupes_from_list':
        # test remove dupes from list
        old = ['a','b','c','a','b','a']
        print (f"old list: {old}")
        new = remove_dupes_from_list(old)
        print (f"new list: {new}")

    if args.action == 'start_time':
        print(start_time)

    if args.action == 'afk':
        print ("AFK...")
        afk()
