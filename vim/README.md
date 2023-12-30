- [Open Files With vim](#open-files-with-vim)
- [Configs](#configs)
  - [Help](#help)
  - [Toggle line numbers](#toggle-line-numbers)
  - [Smart Indent](#smart-indent)
  - [colorscheme](#colorscheme)
- [Tips](#tips)
  - [Search text](#search-text)
  - [Go to line number](#go-to-line-number)
- [vimrc example](#vimrc-example)

---
# Open Files With vim
Open file to particular line number.
```shell
vi +{line_number} {file}

# example: open foo.sh file to line 8:
vi +8 foo.sh
```

Open file to particular function.
```shell
vim +/{myFunctionName} {file}
```

# Configs
## Help
Call for help
```
:help
```

## Toggle line numbers
```
:set number
or
:set nu
```

## Smart Indent
Indent correct amount depending on language and other code indents:
```
:set smartindent
```

## colorscheme
Check colorscheme
```
:colorscheme
```

View colorschemes by following the command with `space` and then `Ctrl+D`
```
:colorscheme
blue       default    desert     evening    koehler    murphy     peachpuff  shine      torte
darkblue   delek      elflord    industry   morning    pablo      ron        slate      zellner
```

# Tips
## Search text
```
/{enter_text_to_search}
```

> Press enter then use `n` to cycle to next found.

## Go to line number
```
:{line_number}

# example: go to line # 14
:14
```

# vimrc example
Save file in root directory as `.vimrc`
```
"Set color scheme
"colorscheme koehler
"colorscheme pablo
"colorscheme ron
colorscheme desert

"enable syntax highlighting
syntax enable

"show line numbers
set number

"set tabs to have 4 spaces
set ts=4

"indent when moving to the next line while writing code
set autoindent

"expand tabs into spaces
set expandtab

"when using the >> or << commands, shift lines by 4 spaces
set shiftwidth=4

"show a visual line under the cursor current line
"set cursorline

"show the matching part of the pair for [] {} and ()
set showmatch

"enable all Python syntax highlighting features
let python_highlight_all = 1

" Encoding
set encoding=utf-8
```
