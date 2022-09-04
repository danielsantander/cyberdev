# Vim Notes


## Open Files With vim
Open file to particular line number.
```shell
vi +<line_number> <file>
```

**Example:** Open `foo.sh` to line 8:
```shell
vi +8 foo.sh
```

Open file to particular function.
```shell
vim +/<myFunctionName> <file>
```

## Set number
List number lines:
```
:set number
```

## Search for some text
Use `/` to search for some given text.

**Example:** Search for "foobar".
```
/foobar
```
> Press enter then use `n` to cycle to next found.

## Go to line number:
```
:<line_number>

# example: go to line # 14
:14
```
