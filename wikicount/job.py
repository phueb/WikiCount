import pickle
import attr
import itertools
from pathos.pools import ProcessPool
from pathlib import Path

from wikicount import configs
from wikicount.count import make_w2dfs


@attr.s
class Params(object):
    wiki_param_name = attr.ib(validator=attr.validators.instance_of(str))
    num_machines = attr.ib(validator=attr.validators.instance_of(int))
    pos = attr.ib(validator=attr.validators.instance_of(str))
    max_num_docs = attr.ib(validator=attr.validators.instance_of(int))
    min_frequency = attr.ib(validator=attr.validators.instance_of(int))

    @pos.validator
    def check(self, _, value):
        if value not in configs.Counting.possible_pos:
            raise ValueError('pos must be in {}'.format(configs.Counting.possible_pos))

    @classmethod
    def from_param2val(cls, param2val):
        """
        instantiate class.
        exclude keys from param2val which are added by Ludwig.
        they are relevant to job submission only.
        """
        kwargs = {k: v for k, v in param2val.items()
                  if k not in ['job_name', 'param_name', 'project_path', 'save_path']}
        return cls(**kwargs)


def main(param2val):  # param2val will be different on each machine

    params = Params.from_param2val(param2val)
    print(params)

    research_data_path = Path(param2val['project_path']).parent
    wiki_param_path = research_data_path / 'CreateWikiCorpus' / 'runs' / params.wiki_param_name
    if not wiki_param_path.exists():
        raise FileNotFoundError('{} does not exist'.format(params.wiki_param_name))

    # load text file
    path_to_articles = list(wiki_param_path.glob('**/bodies.txt'))[0]

    # make generator that iterates over docs in chunks (to use with spacy.nlp.pipe)
    # note: because params.max_num_docs is the number of total docs requested across all jobs,
    # "docs_in_job" is the number of docs needed to process in this job
    docs_in_job = params.max_num_docs // params.num_machines
    f = itertools.islice(path_to_articles.open('r'), docs_in_job)
    texts = [doc for doc in zip(*(f,) * configs.MultiProcessing.num_texts_per_process)]
    num_texts = len(texts)
    print('Number of text chunks: {}'.format(num_texts))

    # count in multiple processes
    pool = ProcessPool(configs.MultiProcessing.num_workers)
    max_num_docs_per_worker = params.max_num_docs // configs.MultiProcessing.num_workers
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
