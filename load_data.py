import json
import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.errors as errors
import azure.cosmos.documents as documents
import azure.cosmos.http_constants as http_constants
import os
import pandas as pd
from textblob import TextBlob

class DataLoader(object):

    def __init__(self):
        with open('config.json') as json_data_file:
            config = json.load(json_data_file)
            self.client = cosmos_client.CosmosClient(url_connection = \
            config["cosmos_url"], auth = {"masterKey": config["cosmos_key"] })

    def load_data(self):
        tweet_collection = 'dbs/' + 'TwitterAnalysis' + '/colls/' + 'tweets'
        query = 'SELECT * FROM c'
        tweet_list = []

        for item in self.client.QueryItems(tweet_collection,
                                      query,
                                      {'enableCrossPartitionQuery': True}
                                      ):
            tweet_list.append(dict(item))

        return tweet_list


    def format_data(self):
        scoped_list = []
        tweet_list = self.load_data()
        for item in tweet_list:
            if item['Tweet']['IsRetweet'] is False and \
            item['Tweet']['QuotedStatusId'] is None and \
            item['Tweet']['InReplyToStatusId'] is None:

                if item['Tweet']['TweetDTO']['extended_tweet'] is not None:
                    text = item['Tweet']['TweetDTO']['extended_tweet']['full_text']
                else:
                    text = item['Tweet']['TweetDTO']['text']

                tb = TextBlob(text)
                result = {
                    "text": text,
                    "polarity": tb.sentiment.polarity,
                    "subjectivity": tb.sentiment.subjectivity,
                    "aboutVirus": ("virus" in text.lower()),
                    "aboutCorona": ("corona" in text.lower() or "covid19" in text.lower()),
                    "aboutResistance": ("resistance" in text.lower()),
                    "timeStamp": pd.Timestamp(item['Timestamp'])
                }
                scoped_list.append(result)


        return pd.DataFrame(scoped_list)
