"""
wiki_param_name is the name of the folder in research_data/CreateWikiCorpus/runs
whose bodies.txt file should be used as text input (e.g. counting words).
"""


param2requests = {
    'wiki_param_name': ['param_{}'.format(21 + i) for i in range(6)],
    'pos': ['ALL'],
    # 'max_num_docs': [1000]
}

# used to overwrite parameters when --debug flag is on (when calling "ludwig-local")
param2debug = {
    'wiki_param_name': 'param_1',
    'max_num_docs': 1000
}


param2default = {
    'wiki_param_name': 'param_1',
    'pos': 'NOUN',
    'max_num_docs': 5 * 1000 * 1000,
    'min_frequency': 2,  # exclude words that occur less than this value in each document
}