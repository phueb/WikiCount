# WikiCount

Research code to count words in English Wikipedia 2018.

## Requirements

* access to the file server at the UIUC Learning & Language Lab is required.
That is where Wikipedia articles are stored.
* [Ludwig](https://github.com/phueb/Ludwig) - a Python package for parallel execution of jobs


## Usage

Use the `ludwig` CLI to run all jobs (on your local machine or remote workers owned by the lab).

```bash
ludwig
```

Each job will do the following: 
One Python pickle file will be saved for each Wikipedia article folder included in the job. 
This file contains a list of Python dictionaries, each containing information about the number of times a word occurs in one article. 

## Compatibility

Tested on Ubuntu 18.04 using Python 3.6.
