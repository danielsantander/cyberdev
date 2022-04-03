# Python Scripts

Directory to hold python script files.

## encryptPDF
Script to encrypt PDF files.

Usage: `./encryptPDF [PDF file] [output location]`

The following will encrypt `tests/sample_data/HelloWorld.pdf` and output the encrypted file in the same directory and the given input (default).
```shell
$ ./encryptPDF.py tests/sample_data/HelloWorld.pdf
Password: 
```

> note: password defaults to 'fairbanks' if none is given when prompted.

Encrypt the same PDF file, but output it in the same directory:
```shell
$ ./encryptPDF.py tests/sample_data/HelloWorld.pdf .
Password:
```
