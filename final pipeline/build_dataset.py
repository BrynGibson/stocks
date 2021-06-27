import pandas as pd
import yfinance as yf
import datetime
import time
import requests
import io
from pathlib import Path
import ast

ticks = ["idex", "amc", "gme", "bb", "uso", "uco", "tsla", "nio"]

base_path = Path.home()/"stonks/data"
data_path = base_path / "counted"

out_path = base_path / "built"
Path.mkdir(out_path, exist_ok=True)

symbol_path = Path("../data/cleaned_listings.csv")

symbol_df = pd.read_csv(symbol_path)

all_files = list(data_path.glob("**/*.csv"))

date_csvs = [d.name.split("_")[-1] for d in all_files]
dates = [d.split(".")[0] for d in date_csvs]
dates = set(dates)
dates = pd.DatetimeIndex(dates)
start_date = dates.min()
end_date = dates.max()


def get_yfinance_data(ticker):
    # download the stock price

    stock = yf.download(ticker, start=start_date, end=end_date, progress=False)

    # append the individual stock prices
    if len(stock) == 0:
        return None
    else:
        stock['Name'] = ticker
        return stock


def count_mentions(ticker, date):

    count_dict = {
        "positive": 0,
        "negative": 0,
        "neutral": 0,
        "total":0
    }

    files = list(data_path.glob(f"**/*{date}.csv"))
    if len(files) == 0:
        return count_dict

    names = {ticker.lower(), symbol_df["fixed_name"].loc[symbol_df["symbol"] == ticker.upper()].values[0].lower()}

    for f in files:
        sent_df = pd.read_csv(f, index_col=0)
        sent_df["entities"] = sent_df["entities"].apply(ast.literal_eval)
        for i in sent_df.index:
            ents = sent_df["entities"].loc[i]

            if names.intersection(set([e.lower() for e in ents])):

                sentiment = sent_df["sentiment"].loc[i]
                print(sentiment)
                if sentiment == 1:
                    count_dict["positive"] += 1
                if sentiment == -1:
                    count_dict["negative"] += 1
                if sentiment == 0:
                    count_dict["neutral"] += 1

    count_dict["total"] = sum(count_dict.values())
    return count_dict


def build_dataset(ticker):
    df = get_yfinance_data(ticker)
    df["positive_mentions"] = None
    df["negative_mentions"] = None
    df["neutral_mentions"] = None
    df["total_mentions"] = None

    for i in df.index:
        mentions = count_mentions(ticker, i.isoformat().split('T')[0])

        df["positive_mentions"].loc[i] = mentions["positive"]
        df["negative_mentions"].loc[i] = mentions["negative"]
        df["neutral_mentions"].loc[i] = mentions["neutral"]
        df["total_mentions"].loc[i] = mentions["total"]

    return df


for tick in ticks:
    gme_df = build_dataset(tick)

    gme_df.to_csv(out_path/f"{tick}.csv")
