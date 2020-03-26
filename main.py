import json
import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.errors as errors
import azure.cosmos.documents as documents
import azure.cosmos.http_constants as http_constants
import os
import pandas as pd
from textblob import TextBlob


with open('config.json') as json_data_file:
    config = json.load(json_data_file)

client = cosmos_client.CosmosClient(url_connection = config["cosmos_url"], auth = {"masterKey": config["cosmos_key"] })
tweet_collection = 'dbs/' + 'TwitterAnalysis' + '/colls/' + 'tweets'
query = 'SELECT * FROM c'
tweet_list = []

for item in client.QueryItems(tweet_collection,
                              query,
                              {'enableCrossPartitionQuery': True}
                              ):
    tweet_list.append(dict(item))

scoped_list = []

for item in tweet_list:
    if item['Tweet']['IsRetweet'] is False and item['Tweet']['QuotedStatusId'] is None and item['Tweet']['InReplyToStatusId'] is None:

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
            "aboutResistance": ("resistance" in text.lower())
        }
        scoped_list.append(result)


df = pd.DataFrame(scoped_list)

# All rows
print("=== Total Rows ===")
print("Rows: " + str(df.shape[0]))
total_polarity_mean = df["polarity"].mean()
print("Polarity mean: " + str(total_polarity_mean))
total_subjectivity_mean = df["subjectivity"].mean()
print("Subjectivity mean: " + str(total_subjectivity_mean))

# Corona rows
print("\n=== Corona Rows ===")
print("Rows: " + str(df.loc[df["aboutCorona"]].shape[0]))
corona_polarity_mean = df.loc[df["aboutCorona"] == True]["polarity"].mean()
print("Corona polarity mean: " + str(corona_polarity_mean))
corona_subjectivity_mean = df.loc[df["aboutCorona"] == True]["subjectivity"].mean()
print("Corona subjectivity mean: " + str(corona_subjectivity_mean))

# Resistance rows
print("\n=== Resistance Rows ===")
print("Rows: " + str(df.loc[df["aboutResistance"]].shape[0]))
resistance_polarity_mean = df.loc[df["aboutResistance"] == True]["polarity"].mean()
print("Resistance polarity mean: " + str(resistance_polarity_mean))
resistance_subjectivity_mean = df.loc[df["aboutResistance"] == True]["subjectivity"].mean()
print("Resistance subjectivity mean: " + str(resistance_subjectivity_mean))

# Virus rows
print("\n=== Virus Rows ===")
print("Rows: " + str(df.loc[df["aboutVirus"]].shape[0]))
resistance_polarity_mean = df.loc[df["aboutVirus"] == True]["polarity"].mean()
print("Virus polariy mean: " + str(resistance_polarity_mean))
resistance_subjectivity_mean = df.loc[df["aboutVirus"] == True]["subjectivity"].mean()
print("Virus subjectivity mean: " + str(resistance_subjectivity_mean))
