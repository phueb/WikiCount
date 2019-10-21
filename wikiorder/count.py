from collections import Counter
from timeit import default_timer as timer
import spacy

from wikiorder import config

nlp = spacy.load('en_core_web_sm')


def make_w2dfs(texts, pos, max_num_docs_per_worker, min_word_freq):
    print('Starting worker')
    start = timer()
    w2dfs = []
    num_processed = 0
    num_skipped = 0
    for doc in nlp.pipe(texts, disable=['parser', 'ner']):

        words = [w.lemma_ for w in doc if pos == config.Counting.no_pos or w.pos_ == pos]

        if not words:
            num_skipped += 1
            continue

        w2df = Counter(words)  # this is very fast
        w2dfs.append({w: f for w, f in w2df.items() if f > min_word_freq})

        num_processed += 1
        if num_processed % 1000 == 0:
            print(num_processed)

        if num_processed == max_num_docs_per_worker:
            break

    print(f'Took {timer() - start} secs to count words with POS={pos} in {num_processed} docs', flush=True)
    print(f'Skipped {num_skipped} docs because they contained no words after filtering', flush=True)
    return w2dfs