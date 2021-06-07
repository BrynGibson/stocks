import pandas as pd
from pathlib import Path
import spacy
from multiprocessing import Pool


base_path = Path(r'C:\Users\sloth\stonks\data')

sub_red = "pennystocks"
out_path = base_path / "parsed" / sub_red

Path.mkdir(out_path, exist_ok=True, parents=True)



sub_path = base_path/sub_red

files = set(sub_path.glob("*.csv"))

done_files = set(out_path.glob("*.csv"))
files = files - done_files





def sent_df(f):

    def sentencize(text):
        doc = nlp(text, disable=bad_pipe)
        sents = [s.text.strip() for s in doc.sents]
        return sents

    df = pd.read_csv(f, index_col=0)
    df = df.dropna(subset=["text"])
    parsed = []
    nlp = spacy.load("en_core_web_sm")
    bad_pipe = ["transformer", "tagger", "ner", "attribute_ruler", "lemmatizer"]
    for i in df["text"]:

        parsed.append(sentencize(i))
    df["parsed"] = parsed

    df.to_csv(out_path/f.name)


# with Pool(6) as p:
#     p.map

for (i,f) in enumerate(files):
    sent_df(f)

    if i % 10 == 0:
        print(f"{i} files done out of {len(files)}")

