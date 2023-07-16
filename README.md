# Leetcode Boilerplate
![GitHub release (with filter)](https://img.shields.io/github/v/release/eric-cc-su/leetcode-boilerplate?filter=*&label=Release)

[![Python 3](https://github.com/eric-cc-su/leetcode-boilerplate/actions/workflows/python.yml/badge.svg)](https://github.com/eric-cc-su/leetcode-boilerplate/actions/workflows/python.yml)

Python scripts to automate Leetcode boilerplate associated with problem-solution creation.

Currently built for Python 3.

## Requirements
- [requests](https://docs.python-requests.org/en/latest/index.html)

## Running Script
```
python3 create_new_problem.py
```

## Usage
```
usage: create_new_problem.py [-h] [--directory DIRECTORY] [--data-structure {None,linked_list,tree}] [--filename FILENAME]

Creates a new Python 3 file with complete boilerplate for a new Leetcode problem that comes with unit testing and support for Leetcode's classes of certain data structures.

options:
  -h, --help            show this help message and exit
  --directory DIRECTORY
                        The directory to create the new file. Default value is the current working directory
  --data-structure {None,linked_list,tree}
                        Data structure to include.
  --filename FILENAME   Provide a manual filename. A filename will be generated in the format 'p#-problem_name.py' if not provided
  --timeout TIMEOUT     Specify a timeout, in seconds, for all requests. Default value is 10s.
  --max-retries MAX_RETRIES
                        Specify a maximum number of retries for failed requests. Default value is 2
```