# Kali Linux Tips & Scripts

Any tips or notes are written in mardown files (`.md` extension) and any executable scripts will be written in shell script files (`.sh`).


## Check Kali Linux Version
```bash
$ lsb_release -a
```


## Useful Tips
### Print Random Line From File
Using the `shuf` utility, print random lines from a file. 
Use the `-n` flag to determine the number of lines to output.
```bash
$ shuf -n 1 <filename>
```