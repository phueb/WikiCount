import pickle
import attr
import itertools
from pathos.pools import ProcessPool
from pathlib import Path

from wikicount import config
from wikicount.count import make_w2dfs


@attr.s
class Params(object):
    wiki_param_name = attr.ib(validator=attr.validators.instance_of(str))
    num_machines = attr.ib(validator=attr.validators.instance_of(int))
    pos = attr.ib(validator=attr.validators.instance_of(str))
    max_num_docs = attr.ib(validator=attr.validators.instance_of(int))
    min_frequency = attr.ib(validator=attr.validators.instance_of(int))
    # ludwig
    param_name = attr.ib(validator=attr.validators.instance_of(str))
    job_name = attr.ib(validator=attr.validators.instance_of(str))

    @pos.validator
    def check(self, _, value):
        if value not in config.Counting.pos_list:
            raise ValueError('pos must be in {}'.format(config.Counting.pos_list))


def main(param2val):  # param2val will be different on each machine

    params = Params(**param2val)
    print(params)

    research_data_path = Path(param2val['project_path']).parent
    wiki_param_path = research_data_path / 'CreateWikiCorpus' / 'runs' / params.wiki_param_name
    if not wiki_param_path.exists():
        raise FileNotFoundError('{} does not exist'.format(params.wiki_param_name))

    # load text file and make generator that iterates over docs in chunks (to use with spacy.nlp.pipe)
    path_to_articles = list(wiki_param_path.glob('**/bodies.txt'))[0]
    f = itertools.islice(path_to_articles.open('r'), params.max_num_docs // params.num_machines)
    texts = [doc for doc in zip(*(f,) * config.MultiProcessing.num_texts_per_process)]
    num_texts = len(texts)
    print('Number of text chunks: {}'.format(num_texts))

    # count in multiple processes
    pool = ProcessPool(config.MultiProcessing.num_workers)
    max_num_docs_per_worker = params.max_num_docs // config.MultiProcessing.num_workers
    results = pool.map(make_w2dfs,
                       texts,  # first arg
                       [params.pos] * num_texts,  # second arg
                       [max_num_docs_per_worker] * num_texts,  # third arg
                       [params.min_frequency] * num_texts  # fourth arg
                       )
    flat_results = [w2df for chunk in results for w2df in chunk]
    print('Num w2dfs: {}'.format(len(flat_results)))

    # save pickled w2dfs to wiki_param_path
    w2dfs_file_name = 'w2dfs_{}_{}.pkl'.format(params.max_num_docs, params.pos)
    full_path = wiki_param_path / w2dfs_file_name
    with full_path.open('wb') as f:
        pickle.dump(flat_results, f)
    print('Saved w2dfs to {}'.format(full_path))

    return []  # Ludwig package requires a list (empty, or containing pandas series objects)
