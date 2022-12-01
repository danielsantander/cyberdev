#!/usr/bin/env python
#!/usr/bin/python3
'''
Script to encrypt PDF file.

USAGE:
$ ./encryptPDF.py <pdf_file_path> <output_path>

WHERE:
    - pdf_file_path is the path of the PDF file to encrypt
    - output_path is optional and will default to the same directory of the
'''

import sys
from pathlib import Path
from getpass import getpass
from utils.file_helper import encrypt_pdf

if __name__ == '__main__':
    # outpath defaults to where the PDF being encrypted is located
    usage = './encryptPDF.py [PDF file] [output path]'

    file = 'default.pdf'
    if (len(sys.argv) < 2):
        sys.exit(f"Unknown operation, USAGE:\t{usage}\n")

    input_pdf_file = sys.argv[1]
    outpath = Path(sys.argv[2]) if len(sys.argv)>2 else None

    try:
        encrypt_pdf(input_pdf_file, pw=getpass(), outpath=outpath)
    except FileNotFoundError:
        sys.exit('File to encrypt not found. Check file name/path.')
    except Exception as e:
        #raise e
        sys.exit('Invalid PDF file.')
