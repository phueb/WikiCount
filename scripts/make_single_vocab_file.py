from pathlib import Path
import pickle
from collections import Counter

from wikicount import configs
from wikicount.params import param2requests, param2default

RESEARCH_DATA_PATH = Path('/') / 'media' / 'research_data'
PARAM_NAMES = param2requests['wiki_param_name']
MAX_NUM_DOCS = param2requests.get('max_num_docs', param2default['max_num_docs'])
POS = 'ALL'

vocab = Counter()

for wiki_param_name in PARAM_NAMES:
    wiki_param_path = RESEARCH_DATA_PATH / 'CreateWikiCorpus' / 'runs' / wiki_param_name
    if not wiki_param_path.exists():
        raise FileNotFoundError('{} does not exist'.format(wiki_param_name))

    # load text file
    fn = f'w2dfs_{MAX_NUM_DOCS}_{POS}.pkl'
    print(f'Loading {fn} in {wiki_param_path}')
    w2dfs_path = list(wiki_param_path.glob(f'**/{fn}'))[0]

    with w2dfs_path.open('rb') as f:
        w2dfs = pickle.load(f)

    # update vocab - one doc/article at a time
    for n, w2df in enumerate(w2dfs):
        vocab.update(w2df)
        if n % 1000 == 0:
            print(f'param={wiki_param_name} | article={n:,}/{MAX_NUM_DOCS:,}')

# save vocab to text file
out_path = configs.Dirs.root / f'vocab_{MAX_NUM_DOCS}_{POS}.txt'
with out_path.open('w') as f:
    f.writelines([f'{f:>12} {w}\n' for w, f in vocab.most_common()])