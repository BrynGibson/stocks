import pandas as pd
from pathlib import Path
import spacy

import re


def remove_bad_chars (vTEXT):
    vTEXT = re.sub(r"(https|http)?:\/\/(\w|\.|/|\?|=|&|%|-)*\b|\\n\\n|\\'", '', vTEXT, flags=re.MULTILINE|re.IGNORECASE)
    return(vTEXT)



#base_path = Path('~/stonks/data')
base_path = Path('C:/Users/sloth/stonks/data')

sub_red = "pennystocks"
out_path = base_path / "clean" / sub_red

Path.mkdir(out_path, exist_ok=True, parents=True)

sub_path = base_path/sub_red

files = set(sub_path.glob("*.csv"))


def sent_df(f):

    df = pd.read_csv(f, index_col=0)
    df = df.dropna(subset=["text"])

    df = df.drop(df.loc[df["text"] == "[removed]"].index)
    df = df.drop(df.loc[df["text"] == "[deleted]"].index)
    df = df.drop(df.loc[df["score"] < 0].index)

    df["cleaned"] = df["text"].apply(remove_bad_chars)

    df.to_csv(out_path/f.name, encoding="utf-8")


for (i, f) in enumerate(files):
    sent_df(f)

    if i % 10 == 0:
        print(f"{i} files done out of {len(files)}")

