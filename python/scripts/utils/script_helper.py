#!/usr/bin/python3

""" Useful methods for scripts. """

import argparse

def get_args(description:str="", debug_mode:bool=False)->argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-d','--debug',
        dest='debug',
        action='store_true',
        default=debug_mode,
        help=f'Debug mode. [{debug_mode}]')
    # return vars(parser.parse_args())
    return parser

