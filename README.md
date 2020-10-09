# WikiCount

Research code to count words in all available English Wikipedia articles.

## Requirements

* access to the file server at the UIUC Learning & Language Lab is required.
That is where Wikipedia articles are stored.
* [Ludwig](https://github.com/phueb/Ludwig) - a Python package for parallel execution of jobs


## Usage

In the terminal:

```bash
ludwig
```

One Python pickle file will be saved for each Wikipedia article folder,
 containing a list of Python dictionaries, 
 each containing information about the number of times a word occurs in one article. 

## Technical Notes

Tested on Ubuntu 18.04 using Python==3.6.
