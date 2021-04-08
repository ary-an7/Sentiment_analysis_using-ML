import tweepy
from textblob import TextBlob
import sys
import csv


 #for this API to work you need to go to developer.twitter.com and create a developer account then generate the below required keys and token.
consumer_key= 'CONSUMER KEY HERE'
consumer_secret= 'CONSUMER SECRET KEY HERE'

access_token='ACCESS KEY HERE'
access_token_secret='ACCESS KEY SECRET HERE'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

public_tweets = api.search('Tesla')

with open('sentiment.csv', 'w', newline='\n') as  f:

	writer = csv.DictWriter(f, fieldnames=['Tweet', 'Sentiment'])
	writer.writeheader()
	for tweet in public_tweets:
		text = tweet.text
			
		analysis = TextBlob(text)

		sentiment = analysis.sentiment.polarity
		if sentiment > 0:
			polarity = 'Positive'
		elif sentiment < 0:
			polarity = 'Negative'
		else:
			polarity = 'Neutral'	

		print(text, polarity)
		print(analysis.sentiment)

		writer.writerow({'Tweet':text, 'Sentiment':polarity})
