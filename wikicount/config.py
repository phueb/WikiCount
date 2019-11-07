from pathlib import Path


class LocalDirs:
    root = Path(__file__).parent.parent


class Global:
    debug = False


class MultiProcessing:
    num_texts_per_process = 100  # do not set higher than 100
    num_workers = 4


class Counting:
    no_pos = 'ALL'
    pos_list = ['PROPN', 'VERB', 'ADP', 'NOUN', 'SYM', 'NUM', no_pos]
