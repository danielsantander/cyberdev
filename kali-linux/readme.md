# Kali Linux Tips & Scripts

Any tips or notes are written in markdown files (`.md` extension) and any executable scripts will be written in shell script files (`.sh`).

Script files will begin with the shebang: `#!/bin/bash`


## Useful Tips

### Check Kali Linux Version
```bash
$ lsb_release -a
```

### Print Random Line From File
Using the `shuf` utility, print random lines from a file. 
Use the `-n` flag to determine the number of lines to output.
```bash
$ shuf -n 1 <filename>
```
