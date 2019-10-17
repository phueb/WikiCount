from collections import Counter
from timeit import default_timer as timer
import spacy

from wikiorder import config

nlp = spacy.load('en_core_web_sm')


def make_w2dfs(texts, pos, max_num_docs_per_worker):
    print('Starting worker')
    start = timer()
    w2dfs = []
    num_processed = 0
    num_skipped = 0
    for doc in nlp.pipe(texts, disable=['parser', 'ner']):

        words = [w.lemma_ for w in doc if pos == config.Counting.no_pos or w.pos_ == pos]

        if not words:
            num_skipped += 0
            continue

        w2df = Counter(words)  # this is very fast
        w2dfs.append(w2df)

        num_processed += 1
        if num_processed % 1000 == 0:
            print(num_processed)

        if num_processed == max_num_docs_per_worker:
            break


    print('Took {} secs to count words with POS={} in {} docs'.format(
        timer() - start, pos, num_processed))
    print('Skipped {} docs because they contained no words after filtering'.format(num_skipped))
    return w2dfs