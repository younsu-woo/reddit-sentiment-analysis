# Reddit Sentiment Analysis
## Project Purpose:question:
To create an interactive dashboard that presents sentiment analysis of a subreddit.
<br><br>

## Project Overview :mag:
This project is intended to dive into the Futurology subreddit to identify sentiment in the top "hot" posts.
<br><br>

## Technology :computer:
- Language: Python
- Data Format: Pandas dataframe
- Data Processing: PRAW, Pandas, nltk, TextBlob
- Visualization: Dash Plotly
<br><br>

## Methodology :memo:
Using the Reddit API, PRAW, we grab the top "hot" subreddit posts' titles, number of comments, and other metrics and store it as a pandas dataframe that will be used in the data pre-processing stage and in future analysis. The dataframe is cleaned prior to categorizing the sentiment. We grab the polarity and subjectivity, and classify the sentiment of each post based on polarity.

This data then feeds in the Dash Plotly dashboard, allowing the end user to choose using the dropdown the visualization they would like to see. The data is updated whenever the Dash app is run for that day and time.
<br><br>

## Visualization :bar_chart:
![Dashboard_Sentiment_Analysis](https://user-images.githubusercontent.com/10111217/230743366-c19fac87-0659-4458-a974-95205f4c395a.png)
