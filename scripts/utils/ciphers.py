#!/usr/bin/env python
#!/usr/bin/python3

""" Methods for utilizing the Caesar Cipher. """

import argparse
import logging
import string
from typing import List


DEFAULT_OFFSET:int = 3
logging.basicConfig(format='%(asctime)s [%(levelname)s]: %(message)s', level=logging.INFO, datefmt='%m/%d/%Y %I:%M:%S %p')

class Caesar:
    def __init__(self, message:str, offset:int=DEFAULT_OFFSET, case_sensitive:bool=False, logger:logging.Logger=None):
        """
        Keyword arguments:

        message (str) -- message to encrypt (required)
        offset (int) -- number of characters in alphabet to shift (default = 3)   # TODO: make default shift random, 1-25.
        case_sensitive (bool) - True to enable case sensitivity. Defaults to False.
        """
        self.message:str = message
        self.offset:int = int(offset) % 26 # keep offset between 0-26
        self.case_sensitive:bool = case_sensitive
        self.encrypted_message = None
        self.decrypted_msg = None

    def encrypt(self)->str:
        """
        Encrypt message with the Caesar Cipher method.
        """
        message = self.message
        word_list:List[str]= message.split() if self.case_sensitive else message.lower().split()

        # alphabet lists
        alpha_lowercase_list = list(string.ascii_lowercase)
        alpha_uppercase_list = list(string.ascii_uppercase)

        cipher_list = []
        for word in word_list:
            cipher_word = ""
            for letter in word:
                alpha_list = alpha_uppercase_list if letter.isupper() else alpha_lowercase_list
                index_num = (alpha_list.index(letter) + self.offset) % len(alpha_list)
                cipher_letter = alpha_list[ index_num ]
                cipher_word += cipher_letter
            cipher_list.append(cipher_word)
        self.encrypted_message = ' '.join(cipher_list)
        return self.encrypted_message

    def decrypt(self)->str:
        """
        Decrypts Caesar Cipher message.
        """
        message = self.message if self.encrypted_message is None else self.encrypted_message
        word_list:List[str] = message.split() if self.case_sensitive else message.lower().split()

        # alphabet lists
        alpha_lowercase_list = list(string.ascii_lowercase)
        alpha_uppercase_list = list(string.ascii_uppercase)

        decrypted_msg = []
        for word in word_list:
            decrypted_word = ""
            for letter in word:
                alpha_list = alpha_uppercase_list if letter.isupper() else alpha_lowercase_list
                index_num = (alpha_list.index(letter) - self.offset) % len(alpha_list)
                decrypted_letter = alpha_list[ index_num ]
                decrypted_word += decrypted_letter
            decrypted_msg.append(decrypted_word)
        self.decrypted_msg = ' '.join(decrypted_msg)
        return self.decrypted_msg

if __name__ == '__main__':

    # Get args
    parser = argparse.ArgumentParser()
    parser.add_argument('msg',
        metavar="msg",
        type=str,
        help="Enter message to encrypt/decrypt.")
    parser.add_argument('--decrypt', '-d',
        action='store_true',
        default=False,
        help="Decrypt message, default is set to False")
    parser.add_argument('--case_sensitive', '-c',
        action='store_true',
        default=False,
        help="Set case sensitivity.")
    parser.add_argument('--offset', '-o',
        nargs="?",
        metavar="offset",
        type=int,
        default=DEFAULT_OFFSET,
        help="Enter the offset value, defaults to 3")

    args = vars(parser.parse_args())
    case_sensitive = args.get('case_sensitive', False)
    msg = args.get('msg', "")
    do_decrypt = args.get('decrypt', False)
    offset = int(args.get('offset', DEFAULT_OFFSET)) % 26   # keep offset between 0-26

    logging.debug(f'case_sensitive:\t{case_sensitive}')
    logging.debug(f'offset:\t{offset}')
    caesar = Caesar(message=msg, offset=offset, case_sensitive=case_sensitive)

    msg = caesar.decrypt() if do_decrypt else caesar.encrypt()
    print(f"{msg}")
