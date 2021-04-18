from pmaw import PushshiftAPI
import datetime
import pandas as pd
from pathlib import Path
from timeit import default_timer as timer
from datetime import timedelta

api = PushshiftAPI()

base_path = Path.home()/"Desktop/stonks"
data_path = base_path/"data"
Path.mkdir(base_path, exist_ok=True)
Path.mkdir(data_path, exist_ok=True)

start_date = datetime.date(year=2020, month=5, day=3)
dates = pd.date_range(start=start_date, end=datetime.datetime.now())

subreddit = "pennystocks"
out_path = data_path / subreddit
Path.mkdir(out_path, exist_ok=True)

start = timer()

for i in range(0, len(dates) -1):

    lap = timer()
    submissions = list(api.search_submissions(after=int(dates[i].timestamp()),
                                              before=int(dates[i + 1].timestamp()),
                                              subreddit=subreddit))

    content =[]
    for post in submissions:
        try:

            content.append([post["title"], post["id"], post["author"], post["full_link"], post["score"], post["num_comments"],
                        post["selftext"], dates[i].date(), post["url"]])
        except:
            continue
    submissions_df = pd.DataFrame(content,
                                  columns=['title', 'id', "author", 'url', 'score', 'num_comments', 'text', 'date',
                                           "link"])
    submissions_df.to_csv(out_path / f"{subreddit}_posts_{dates[i].date()}.csv")

    sub_ids = submissions_df["id"].loc[submissions_df["num_comments"] > 0].values
    comment_ids = api.search_submission_comment_ids(ids=sub_ids)
    comments = list(api.search_comments(ids=comment_ids))

    content = []

    for post in comments:
        try:
            content.append([post["author"], post["id"], post["permalink"], post["score"], post["body"], dates[i].date()])
        except:
            continue
    comments_df = pd.DataFrame(content, columns=['author', 'id', 'url', 'score', 'text', 'date'])
    comments_df.to_csv(out_path / f"{subreddit}_comments_{dates[i].date()}.csv")


    if i % 5 == 0:
        end = timer()
        print(f"{i} days scraped out of {len(dates)}")
        print(f"{timedelta(seconds=end-start)} elapsed out of eta {timedelta(seconds=end-(lap*(len(dates)/5)))}")
