#!/usr/bin/python3
""" Methods for utilizing the Caesar Cipher. """

import logging
import string
import sys

# logging.basicConfig(format='%(asctime)s [%(levelname)s]: %(message)s', level=logging.INFO, datefmt='%m/%d/%Y %I:%M:%S %p')

def encrypt(message:str, offset:int=3, case_sensitive:bool=False)->str:
    """ Encrypt message with the Caesar Cipher method.

    Keyword arguments:
    message -- message to encrypt (required)
    offset -- number of characters in alphabet to shift (default = 3)
    """
    if (offset > 25 or offset < 0): raise Exception('Invalid offset value. Offset must be between 0-25')
    word_list = message.split() if case_sensitive else message.lower().split()
    alpha = list(string.ascii_letters) if case_sensitive else list(string.ascii_lowercase)
    alpha_offset = alpha.copy()
    # for x in range(len(alpha)):
    #     new_index = (x+offset) % len(alpha)
    #     alpha_offset[x] = alpha[new_index]
    # IN ONE LINE:
    alpha_offset = [ alpha[(x+offset)%len(alpha)] for x in range(len(alpha)) ]

    cipher_list = []
    for word in word_list:
        cipher_word = ""
        for letter in word:
            cipher_letter = alpha_offset[ alpha.index(letter) ]
            cipher_word += cipher_letter
        cipher_list.append(cipher_word)
    return ' '.join(cipher_list)


def decrypt(message:str, offset:int, case_sensitive:bool=False)->str:
    """ Decrypts Caesar Cipher message.

    Keyword arguments:
    message -- message to decrypt
    offset -- number of characters in alphabet to shift
    """
    if (offset > 25 or offset < 0): raise Exception('Invalid offset value. Offset must be between 0-25')
    word_list = message.split() if case_sensitive else message.lower().split()
    alpha = list(string.ascii_letters) if case_sensitive else list(string.ascii_lowercase)
    alpha_offset = [ alpha[(x-offset)%len(alpha)] for x in range(len(alpha)) ]

    decrypted_msg = []
    for word in word_list:
        decrypted_word = ""
        for letter in word:
            decrypted_letter = alpha_offset[alpha.index(letter)]
            decrypted_word += decrypted_letter
        decrypted_msg.append(decrypted_word)
    return ' '.join(decrypted_msg)
