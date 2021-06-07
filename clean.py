import pandas as pd
from pathlib import Path
import spacy

import re


def remove_urls (vTEXT):
    vTEXT = re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%|\-)*\b', '', vTEXT, flags=re.MULTILINE)
    return(vTEXT)

base_path = Path(r'C:\Users\sloth\stonks\data')

sub_red = "pennystocks"
out_path = base_path / "clean" / sub_red

Path.mkdir(out_path, exist_ok=True, parents=True)



sub_path = base_path/sub_red

files = set(sub_path.glob("*.csv"))

# done_files = set(out_path.glob("*.csv"))
# files = files - done_files





def sent_df(f):

    df = pd.read_csv(f, index_col=0)
    df = df.dropna(subset=["text"])
    clean = []

    df = df.drop(df.loc[df["text"] == "[removed]"].index)
    df = df.drop(df.loc[df["text"] == "[deleted]"].index)
    df = df.drop(df.loc[df["score"] < 0].index)

    for i in df["text"]:
        clean.append(remove_urls(i))
    df["cleaned"] = clean

    df.to_csv(out_path/f.name, encoding="utf-8")


# with Pool(6) as p:
#     p.map

for (i,f) in enumerate(files):
    sent_df(f)

    if i % 10 == 0:
        print(f"{i} files done out of {len(files)}")

