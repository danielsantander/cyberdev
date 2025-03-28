- [Configs](#configs)
- [Tips](#tips)


```shell
# open file
vi {file} +number

# open foo.sh file to line 8:
vi foo.sh +8

# open file based on keyword search
vim {file} +/keyword

write/save and exit
:wq

exit
:q

force quit
:q!
```

# Configs

```shell
# call for help
:help

# toggle line numbers
:set number
# or
:set nu

# Smart Indent -- indent correct amount depending on language and other code indents:
:set smartindent
```

# Tips

```shell
# search text by keyword -- press enter then use `n` to cycle to next found
/keyword

# go to line number
:line_number
```
