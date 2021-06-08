from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import numpy as np
import pandas as pd
from pathlib import Path
import ast
from timeit import default_timer as timer
from datetime import timedelta



def get_sentiment(text):

    class_names = [-1, 0, 1]

    encoded_new = tokenizer.encode_plus(
                            text,                      # Sentence to encode.
                            add_special_tokens = True,
                            max_length=512,# Add '[CLS]' and '[SEP]'            # Pad & truncate all sentences.
                            padding = True,
                            return_attention_mask = True,     # Construct attn. masks.
                            return_tensors = 'pt',
                            truncation=True# Return pytorch tensors.
                       )

    # Add the encoded sentence to the list.
    input_idst = (encoded_new['input_ids'])
    attention_maskst = (encoded_new['attention_mask'])

    # Convert the lists into tensors.
    input_idst = torch.cat([input_idst], dim=0)
    attention_maskst = torch.cat([attention_maskst], dim=0)


    new_test_output = model(input_idst, token_type_ids=None,
                          attention_mask=attention_maskst)

    logits = new_test_output[0]
    predicted = logits.detach().numpy()

    # Store predictions
    flat_predictions = np.concatenate(predicted, axis=0)

    # For each sample, pick the label (0 or 1) with the higher score.
    new_predictions = np.argmax(flat_predictions).flatten()

    return class_names[new_predictions[0]]

def sent_file(f):
    df = pd.read_csv(f, index_col=0)
    df = df.dropna(subset=["cleaned"])

    df["sentiment"] = df["cleaned"].apply(get_sentiment)
    # sented = []
    #
    # for i in df["cleaned"]:
    #
    #     sented.append(get_sentiment(i))
    #
    # df["sentiment"] = sented

    df.to_csv(out_path / f.name, encoding="utf-8")

if __name__ == "__main__":


    #base_path = Path('~/stonks/data')
    base_path = Path('C:/Users/sloth/stonks/data')

    sub_red = "pennystocks"
    parsed_path = base_path / "clean"


    out_path = base_path / "sentiment" / sub_red

    Path.mkdir(out_path, exist_ok=True, parents=True)

    sub_path = parsed_path / sub_red

    files = set(sub_path.glob("*.csv"))

    done_files = set(out_path.glob("*.csv"))
    files = files - done_files

    tokenizer = AutoTokenizer.from_pretrained("ipuneetrathore/bert-base-cased-finetuned-finBERT")
    model = AutoModelForSequenceClassification.from_pretrained("ipuneetrathore/bert-base-cased-finetuned-finBERT")

    for (i, f) in enumerate(files):
        print(f"starting file {f.name}")
        start = timer()
        sent_file(f)
        end = timer()
        print(f"one file took {timedelta(seconds=end - start)}")

        if i % 10 == 0:
            print(f"{i} files done out of {len(files)}")