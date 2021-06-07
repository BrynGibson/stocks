import pandas as pd
import numpy as np
from pathlib import Path
import re


base_path = Path(r'C:\Users\sloth\stonks\data')

sub_red = "pennystocks"
parsed_path = base_path / "sentiment"

out_path = base_path / "counted" / sub_red

Path.mkdir(out_path, exist_ok=True, parents=True)

sub_path = parsed_path / sub_red

files = set(sub_path.glob("*.csv"))

done_files = set(out_path.glob("*.csv"))
files = files - done_files

tickers_path = Path("./data/listing_status.csv")

tickers_df = pd.read_csv(tickers_path)