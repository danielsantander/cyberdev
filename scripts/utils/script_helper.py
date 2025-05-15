#!/usr/bin/python3

""" Useful methods for scripts. """

import argparse

def get_args(debug_mode:bool=False, **kwargs)->argparse.ArgumentParser:
    parser = argparse.ArgumentParser(**kwargs)
    parser.add_argument('-d','--debug',
        dest='debug',
        action='store_true',
        default=debug_mode,
        help=f'Debug mode. [{debug_mode}]')
    parser.add_argument('-i', '--input',
        dest='input',
        metavar='PATH',
        action='store',
        type=str,
        help='Source path of input file/directory.')
    parser.add_argument('-o', '--output',
        dest='output',
        metavar='PATH',
        action="store",
        type=str,
        help='Destination path of output file/directory.')
    # return vars(parser.parse_args())
    return parser

