*Table of Contents*
- [Usage](#usage)
  - [Options](#options)
- [Find File by Name or Extension](#find-file-by-name-or-extension)
- [Find File Based on Content](#find-file-based-on-content)
  - [Search for content with Regular Expressions](#search-for-content-with-regular-expressions)
- [Sources \& References](#sources--references)

# Usage
Usage: `find <directory> <options> <expression>`
```shell
$ find . -name "pattern" -print
```

## Options
`-atime <number_of_days>` file was accessed a given number of days ago

`-mtime <number_of_days>` file was modified a given number of days ago

`-size <file_size_in_blocks> ` files in a given number of blocks big (a block is 512 bytes)

`-type <file_type>` Specifies file type: f=plain text, d=directory


# Find File by Name or Extension
Use `find` from the command line to locate a specific file by name or extention. The following example searchs for the `*.err` files in the `/home/username/` directory and all sub-directories:

```bash
$ find /home/username/ -name "*.err"
```

# Find File Based on Content
The `find` command can only filter the directory hierarchy based on a file's name and metadata. If you need to search based on the file's content, use a tool like `grep`.

**Example:** Use `grep` to find a file based on content
```shell
$ find . -type f -exec grep "example-text-content-to-search" '{}' \; -print
```
This searches every object in the current directory hierarchy (`.`) that is a file (`-type f`) and then runs the command `grep "example"` for every file that satisfies the conditions. The files that match are printed on the screen (`-print`). The curly braces (`{}`) are a placeholder for the `find` match results. The `{}` are enclosed in a single quotes (`'`) to avoid handing `grep` a malformed file name. The `-exec` command is terminated with a semicolon (`;`), which should be escaped (`\;`) to avoid interpretation by the shell.


## Search for content with Regular Expressions
Here is an example of using `find` and `grep` commands with regular expressions to search the current directory for a file anywhere the text "TableOrderingFilter" may be present.

```shell
$ find . -type f -exec grep "\w*[T|t]able[O|o]rdering[F|f]ilter\w*" '{}' \; -print

# Anywhere there is "OrderingFilter" that does not begin with a period
$ find . -type f -exec grep "[^\.]*[O|o]rdering[F|f]ilter\w*" '{}' \; -print
```

# Sources & References

https://kb.iu.edu/d/admm

https://www.linode.com/docs/guides/find-files-in-linux-using-the-command-line/

https://www.geeksforgeeks.org/find-command-in-linux-with-examples/


