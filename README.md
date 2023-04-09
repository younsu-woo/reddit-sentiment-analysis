# Reddit Sentiment Analysis
## Project Purpose:question:
To create an interactive dashboard that presents real-time sentiment analysis of a subreddit feed. 
<br><br>

## Project Overview :mag:
This project is intended to dive into the Futurology subreddit to identify sentiment in the top "hot" posts. The web app is deployed on PythonAnywhere <a href="http://roguelash.pythonanywhere.com" title="here">here</a>. 

There are six elements of the visualization component:
1. Word cloud
2. Overall sentiment 
3. Frequency table
4. Frequency chart
5. Polarity and Subjectivity
6. Posts by Sentiment
<br><br>

## Technology :computer:
- Language: Python
- Data Format: Pandas dataframe
- Data Processing: PRAW, Pandas, nltk, TextBlob
- Visualization: Dash Plotly
<br><br>

## Methodology :memo:
Using the Reddit API, PRAW, we grab the top "hot" subreddit posts' titles, number of comments, and other metrics and store it as a pandas dataframe that will be used in the data pre-processing stage and in future analysis. The dataframe is cleaned prior to categorizing the sentiment. We grab the polarity and subjectivity, and classify the sentiment of each post based on polarity.

This data then feeds in the Dash Plotly dashboard, allowing the end user to choose using the dropdown the visualization they would like to see. The data is updated whenever the app is run, and pulls updated data whenever the page is refreshed.
<br><br>

## Visualization :bar_chart:
![Dashboard_Sentiment_Analysis](https://user-images.githubusercontent.com/10111217/230750792-8132cbe2-8557-4507-b7b8-c38af880b1e7.png)
