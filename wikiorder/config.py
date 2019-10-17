from pathlib import Path
import sys

if sys.platform == 'darwin':
    mnt_point = '/Volumes'
elif 'linux' == sys.platform:
    mnt_point = '/media'
else:
    raise SystemExit('Ludwig does not support this platform')


class RemoteDirs:
    research_data = Path(mnt_point) / 'research_data'
    root = research_data / 'WikiOrder'
    runs = root / 'runs'
    wiki = research_data / 'CreateWikiCorpus'


class LocalDirs:
    root = Path(__file__).parent.parent
    src = root / 'wikiorder'
    runs = root / '{}_runs'.format(src.name)

    wiki = Path('/home/ph/CreateWikiCorpus')  # user must edit this


class Global:
    debug = False


class MultiProcessing:
    num_texts_per_process = 100  # TODO
    num_workers = 4


class Counting:
    no_pos = 'ALL'
    pos_list = ['PROPN', 'VERB', 'ADP', 'NOUN', 'SYM', 'NUM', no_pos]