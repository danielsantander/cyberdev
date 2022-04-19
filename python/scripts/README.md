*Python Scripts Table of Contents*
- [encryptPDF.py](#encryptpdfpy)

# encryptPDF.py
Python script for encrypting PDF files.

Usage: `./encryptPDF [PDF file] [output location]`

> Password defaults to 'fairbanks' if not given when prompted.

**Example**: Encrypt `tests/sample_data/pdfs/HelloWorld.pdf` and output the encrypted file in the same directory as the file to encrypt.
There should then be an encrypted PDF file located at `tests/sample_data/pdfs/HelloWorldENCRYPTED.pdf`.
```shell
$ ./encryptPDF.py tests/sample_data/pdfs/HelloWorld.pdf
Password: 
```

**Example**: Encrypt the same PDF file, but output it in the current directory.
There should then be an encrypted PDF file located in the current directory named `HelloWorldENCRYPTED.pdf`.
```shell
$ ./encryptPDF.py tests/sample_data/pdfs/HelloWorld.pdf .
Password:
```
