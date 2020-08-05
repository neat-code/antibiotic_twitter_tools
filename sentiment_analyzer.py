import json
import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.errors as errors
import azure.cosmos.documents as documents
import azure.cosmos.http_constants as http_constants
import os
import pandas as pd
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer

class SentimentAnalyzer(object):

    def __init__(self):
        with open('config.json') as json_data_file:
            config = json.load(json_data_file)
            self.client = cosmos_client.CosmosClient(url_connection = \
            config["cosmos_url"], auth = {"masterKey": config["cosmos_key"] })

    def load_data(self):
        tweet_collection = 'dbs/' + 'TwitterAnalysis' + '/colls/' + 'tweets'
        sentiment_collection = 'dbs/' + 'TwitterAnalysis' + '/colls/' + 'sentimentAnalysis'
        query = 'SELECT * FROM c'

        for item in self.client.QueryItems(tweet_collection,
                                      query,
                                      {'enableCrossPartitionQuery': True}
                                      ):
              result = self.format_data(item)
              if result is not None:
                  print(result)
                  self.client.UpsertItem(sentiment_collection, self.format_data(item))
                  print("Item upserted")





    def format_data(self, item):
            if item['Tweet']['IsRetweet'] is False and \
            item['Tweet']['QuotedStatusId'] is None and \
            item['Tweet']['InReplyToStatusId'] is None:

                if item['Tweet']['TweetDTO']['extended_tweet'] is not None:
                    text = item['Tweet']['TweetDTO']['extended_tweet']['full_text']
                else:
                    text = item['Tweet']['TweetDTO']['text']

                tb = TextBlob(text, analyzer=NaiveBayesAnalyzer())
                return {
                    "id": item['id'],
                    "PartitionKey": item['PartitionKey'],
                    "text": text,
                    "sentiment_classification": tb.sentiment.classification,
                    "sentiment_pos": tb.sentiment.p_pos,
                    "sentiment_neg": tb.sentiment.p_neg,
                    "subjectivity": tb.subjectivity,
                    "aboutVirus": ("virus" in text.lower()),
                    "aboutCorona": ("corona" in text.lower() or "covid19" in text.lower()),
                    "aboutResistance": ("resistance" in text.lower()),
                    "timeStamp": item['Timestamp']
                }
