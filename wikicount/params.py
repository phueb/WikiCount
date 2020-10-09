"""
wiki_param_name is the name of the folder in research_data/CreateWikiCorpus/runs
whose bodies.txt file should be used as text input (e.g. counting words).
"""

num_wiki_folders = 6  # each folder contains one text file containing multiple articles

param2requests = {
    'wiki_param_name': ['param_{}'.format(22 + i) for i in range(num_wiki_folders)],
    'pos': ['ALL'],
}

# used to overwrite parameters when --debug flag is on (when calling "ludwig-local")
param2debug = {
    'wiki_param_name': 'param_1',
    'max_num_docs': 48 * 100
}


param2default = {
    'wiki_param_name': 'param_1',
    'num_machines': num_wiki_folders,
    'pos': 'ALL',
    'max_num_docs': 48 * 100 * 1000,  # total number of docs across all jobs
    'min_frequency': 2,  # exclude words that occur less than this value in each document
}

if 'max_num_docs' in param2requests:
    for v in param2requests['max_num_docs']:
        assert v % num_wiki_folders == 0

assert param2debug['max_num_docs'] % num_wiki_folders == 0
assert param2default['max_num_docs'] % num_wiki_folders == 0