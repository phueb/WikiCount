from pathlib import Path


class Dirs:
    root = Path(__file__).parent.parent


class MultiProcessing:
    num_texts_per_process = 100  # do not set higher than 100
    num_workers = 4


class Counting:
    possible_pos = ['PROPN', 'VERB', 'ADP', 'NOUN', 'SYM', 'NUM', 'ALL']
