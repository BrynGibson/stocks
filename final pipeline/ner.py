from flair.data import Sentence
from flair.models import SequenceTagger
import spacy
import pandas as pd
import numpy as np
from pathlib import Path
from timeit import default_timer as timer
from datetime import timedelta


#base_path = Path('~/stonks/data')
base_path = Path('C:/Users/sloth/stonks/data')

sub_red = "pennystocks"
out_path = base_path / "counted" / sub_red

Path.mkdir(out_path, exist_ok=True, parents=True)



sub_path = base_path/"sentiment"/sub_red

files = set(sub_path.glob("*.csv"))

done_files = set(out_path.glob("*.csv"))
files = files - done_files

# load tagger
tagger = SequenceTagger.load("flair/ner-english-large")

nlp = spacy.load("en_core_web_sm")
bad_pipe = ["transformer", "tagger", "ner", "attribute_ruler", "lemmatizer"]


def sentencize(text):
    doc = nlp(text, disable=bad_pipe)
    sents = [s.text.strip() for s in doc.sents]
    return sents


def get_entities(post):

    entities = set()

    split = sentencize(post)
    sents = [Sentence(s) for s in split if s]
    tagger.predict(sents)
    for s in sents:
        orgs = [n.text for n in s.get_spans("ner")]
        entities.update(orgs)

    return list(entities)


def tag_file(f):
    start = timer()
    print(f"starting file {f.name}")

    df = pd.read_csv(f, index_col=0)

    df["entities"] = df["cleaned"].apply(get_entities)

    df.to_csv(out_path/f.name, encoding="utf-8")
    end = timer()
    print(f"one file took {timedelta(seconds=end - start)}")

for f in files:
    tag_file(f)