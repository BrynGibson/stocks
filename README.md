### Reddit investor groups sentiment analysis

This respository contains code used for a project that involved scraping Reddit comments and posts from investing related Subreddit pages.

The scraped data was then cleaned and and sentencized using NLTK and Spacy.

This data was then passed into a pipeline of transformer based natural language processing models to identify all companies, groups or individuals mentioned and
the positivity of the mentioned group / individual. 

Next these mentioned groups, individuals or companies were compared against a known list of company names and tickers. This allowed me to build up a data set
showing the number of mentions and the general sentiment of Reddit users towards publicly traded companies. 

Once a sentiment overtime dataset had been built up exploratory analysis could then be done to explore the relationship between these mentions and stock price movements.
