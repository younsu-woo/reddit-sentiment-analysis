import pandas as pd
import numpy as np
import re
import praw
from textblob import TextBlob
from wordcloud import WordCloud, STOPWORDS
from nltk.corpus import stopwords
import nltk
import warnings
import operator
import matplotlib.pyplot as plt
import base64
import operator
from io import BytesIO

def grab_subreddit_sentiment():
    user_agent = 'Reddit_Scrapper 1.0 by /u//FeatureChoice5036'

    reddit = praw.Reddit(
        client_id='my-client-id',
        client_secret='my-client-secret',
        user_agent=user_agent
    )

    headlines = []
    date_created = []
    avg_score = []
    upvote_ratio = []
    num_comments = []
    num_awards = []
    pinned = []

    for submission in reddit.subreddit('futurology').hot(limit=None):
        headlines.append(submission.title)
        date_created.append(submission.created_utc)
        avg_score.append(submission.score)
        upvote_ratio.append(submission.upvote_ratio)
        num_comments.append(submission.num_comments)
        num_awards.append(submission.total_awards_received)
        pinned.append(submission.pinned)

    reddit_df = pd.DataFrame({'Title': headlines,
                              'Date': date_created,
                              'Average Score': avg_score,
                              'Upvote Ratio': upvote_ratio,
                              'Number of Comments': num_comments,
                              'Awards Received': num_awards,
                              'Pinned': pinned
                             })

    # Delete 'Pinned' column as it's no longer required
    reddit_df = reddit_df.drop('Pinned', axis=1)

    # Delete duplicate posts
    reddit_df = reddit_df.drop_duplicates(subset='Title', keep='first')
    reddit_df.Title.duplicated().sum()

    # Convert 'Date' column from Unix epoch to datetime
    reddit_df['Date'] = pd.to_datetime(reddit_df['Date'],unit='s').dt.date

    def text_clean(text):
        text = re.sub(r"(?<!\d)[.,;:](?!\d)", '', text, 0)  # Remove all punctuation except in digits
        text = re.sub(r'https?:\/\/\S+', '', text)  # Remove the hyperlinks
        emoji_pattern = re.compile("["
                                   u"\U0001F600-\U0001F64F"  # emoticons
                                   u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                   u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                   u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                   "]+", flags=re.UNICODE)
        text = emoji_pattern.sub(r'', text)  # Remove emojis

        return text

    # Cleaning the text
    reddit_df['Title'] = reddit_df['Title'].apply(text_clean)

    # Create a function to get Subjectivity
    def getSubjectivity(text):
        return TextBlob(text).sentiment.subjectivity
    # Create a function to get Polarity
    def getPolarity(text):
        return TextBlob(text).sentiment.polarity

    # Create new column for what we just did and add it to reddit_df dataframe
    reddit_df['Subjectivity'] = reddit_df['Title'].apply(getSubjectivity)
    reddit_df['Polarity'] = reddit_df['Title'].apply(getPolarity)

    # Group the range of Polarity into different categories
    def getSentiment(score):
        if score < 0:
            return 'Negative'
        elif score == 0:
            return 'Neutral'
        else:
            return 'Positive'

    reddit_df['Sentiment'] = reddit_df['Polarity'].apply(getSentiment)

    return reddit_df


def create_wordcloud(reddit_df):
    # Stopwords to filter out
    stopwords_wc = STOPWORDS
    stopwords_all = list(set(list(stopwords_wc) + stopwords.words('english')))

    # Create word cloud
    text = ' '.join([posts for posts in reddit_df['Title']])
    freq_dict = WordCloud(stopwords=stopwords_all).process_text(text)
    wc = WordCloud(width=450, height=270,
                   max_words=100,
                   background_color='white').generate_from_frequencies(frequencies=freq_dict)
    wc_img = wc.to_image()
    with BytesIO() as buffer:
        wc_img.save(buffer, 'png')
        img2 = base64.b64encode(buffer.getvalue()).decode()

    return img2

def create_freq_df(reddit_df):
    # Stopwords to filter out
    stopwords_wc = STOPWORDS
    stopwords_all = list(set(list(stopwords_wc) + stopwords.words('english')))

    # Create word cloud
    text = ' '.join([posts for posts in reddit_df['Title']])
    freq_dict = WordCloud(stopwords=stopwords_all).process_text(text)

    # Create frequency dataframe
    sorted_freq_dict = dict(sorted(freq_dict.items(), key=operator.itemgetter(1), reverse=True))
    sorted_freq_df = pd.DataFrame(sorted_freq_dict.items(), columns=['Word', 'Frequency'])

    return sorted_freq_df