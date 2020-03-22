import json
import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.errors as errors
import azure.cosmos.documents as documents
import azure.cosmos.http_constants as http_constants
import os
from textblob import TextBlob
from classes.sentiment_result import SentimentResult


with open('config.json') as json_data_file:
    config = json.load(json_data_file)

client = cosmos_client.CosmosClient(url_connection = config["cosmos_url"], auth = {"masterKey": config["cosmos_key"] })
collection_link = 'dbs/' + 'TwitterAnalysis' + '/colls/' + 'tweets'
query = 'SELECT TOP 10 * FROM c'
tweet_list = []

for item in client.QueryItems(collection_link,
                              query,
                              {'enableCrossPartitionQuery': True}
                              ):
    tweet_list.append(dict(item))

scoped_list = []

for item in tweet_list:
    if item['Tweet']['IsRetweet'] is False and item['Tweet']['QuotedStatusId'] is None and item['Tweet']['InReplyToStatusId'] is None:
        text = ""
        if item['Tweet']['TweetDTO']['extended_tweet'] is not None:
            text = item['Tweet']['TweetDTO']['extended_tweet']['full_text']
        else:
            text = item['Tweet']['TweetDTO']['text']

        tb = TextBlob(text)
        scoped_list.append(SentimentResult(text, tb.sentiment))
