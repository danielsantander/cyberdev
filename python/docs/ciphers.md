
- [Caesar Cipher](#caesar-cipher)
  - [Encrypt Caesar Cipher](#encrypt-caesar-cipher)
  - [Decrypt Caesar Cipher](#decrypt-caesar-cipher)
- [Sources](#sources)

# Caesar Cipher

A simple cipher that encrypts messages by replacing each letter with a new value determined by shifting the alphabet over a given offset value.

For example, with an offset value of 3 every A would be replaced by the letter D, every B with the letter E, every C with the letter F, and so on...

## Encrypt Caesar Cipher

Using the Caesar cipher to encrypt a message without defining an offset value will default to shifting the message 3 alphabet letters.

For example, encrypting `Hello World` with the Caesar cipher and a default offset value of 3 will output `khoor zruog`.

```python
from utils.ciphers import caesar
caesar.encrypt("Hello World")

>>> 'khoor zruog'
```

Defining an offset of 15 will encrypt the message by shifting the alphabet 15 letters. Encrypting `Hello World` with an offset of 15 will return `wtaad ldgas`

```python
from utils.ciphers import caesar
caesar.encrypt("Hello World", offset=15)

>>> 'wtaad ldgas'
```

## Decrypt Caesar Cipher

Decrypting a Caesar cipher message requires the known offset value.

For example, decrypting the message `amkzmb umaaiom` will need an offset value of 8.

```python
from utils.ciphers import caesar
caesar.decrypt('amkzmb umaaiom', offset=8)

>>> 'secret message'
```

# Sources

Cracking Codes With Python.
