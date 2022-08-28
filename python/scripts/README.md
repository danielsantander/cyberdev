*Python Scripts Table of Contents*
- [encryptPDF.py](#encryptpdfpy)
- [rename_files.py](#rename_filespy)

# encryptPDF.py
Python script for encrypting PDF files.

Usage: `./encryptPDF [PDF file] [output location]`

> pw defaults to 'fairbanks' if not given when prompted

**Example**: Encrypt `tests/sample_data/pdfs/HelloWorld.pdf` and output the encrypted file in the same directory as the file to encrypt.
There should then be an encrypted PDF file located at `tests/sample_data/pdfs/HelloWorldENCRYPTED.pdf` (outputs in same directory as the input file).
```shell
$ ./encryptPDF.py tests/sample_data/pdfs/HelloWorld.pdf
```

**Example**: Encrypt the same PDF file, but send output to the current directory.
There should then be an encrypted PDF file located in the current directory named `HelloWorldENCRYPTED.pdf`.
```shell
$ ./encryptPDF.py tests/sample_data/pdfs/HelloWorld.pdf .
```

# rename_files.py
run in debug mode:
```shell
./rename_files.py <filepath> -i --debug --preface="preface_filename_with_this__"
```