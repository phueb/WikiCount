"""
wiki_param_name is the name of the folder in research_data/CreateWikiCorpus/runs
whose bodies.txt file should be used as text input (e.g. counting words).
"""

NUM_LUDWIG_WORKERS = 6

param2requests = {
    'wiki_param_name': ['param_{}'.format(21 + i) for i in range(NUM_LUDWIG_WORKERS + 1)],
    'pos': ['ALL'],
    'max_num_docs': [48 * 100]
}

# used to overwrite parameters when --debug flag is on (when calling "ludwig-local")
param2debug = {
    'wiki_param_name': 'param_1',
    'max_num_docs': 48 * 100
}


param2default = {
    'wiki_param_name': 'param_1',
    'num_machines': NUM_LUDWIG_WORKERS,
    'pos': 'NOUN',
    'max_num_docs': 48 * 100 * 1000,  # total number of docs across all jobs
    'min_frequency': 2,  # exclude words that occur less than this value in each document
}

if 'max_num_docs' in param2requests:
    for v in param2requests['max_num_docs']:
        assert v % NUM_LUDWIG_WORKERS == 0

assert param2debug['max_num_docs'] % NUM_LUDWIG_WORKERS == 0
assert param2default['max_num_docs'] % NUM_LUDWIG_WORKERS == 0