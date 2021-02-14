# greppetto
A simple python script to search patterns in files and print the matching lines using different formats.

# Running the script
```
./greppetto.py --help
usage: greppetto.py [-h] -r REGEX [-f [FILE ...]] [-u | -c | -m]

optional arguments:
  -h, --help            show this help message and exit
  -r REGEX, --regex REGEX
                        regexp to search
  -f [FILE ...], --files [FILE ...]
                        files to read, if empty, stdin is used
  -u, --underscore      prints '^' under the matching text
  -c, --color           highlight the matching text
  -m, --machine         generate machine-readable output format: file_name:no_line:start_pos:matched_text

```

# Examples:
```
# Search for mypattern in one file and print the matching lines
./greppetto.py -r mypattern  -f ./test_files/testfile01.log

# Search for the regular expression "my[a-z]*" in multiple files and highlight it with color
./greppetto.py -r "my[a-z]*"  -f  test_files/testfile0*.log -c

# Search for INFO in stdin and underscore with ^^^ all occurrences
cat /var/log/dnf.log | ./greppetto.py  -r INFO -u

# Search for DEBUG in a file and print the matching lines with a machine readable format:
./greppetto.py  -r DEBUG -f /var/log/dnf.log -m
```