import json
import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.errors as errors
import azure.cosmos.documents as documents
import azure.cosmos.http_constants as http_constants
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from textblob import TextBlob
from matplotlib.pyplot import subplot, figure

def update_histogram(dataframe, metric_column, figure_number, title):
    chart = plt.subplot(2, 4, figure_number)
    chart.hist(dataframe[metric_column])
    chart.set_title(title)

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

# Total Rows
update_histogram(df, "polarity", 1, "Total Polarity")
update_histogram(df, "subjectivity", 2, "Total Subjectivity")

# Virus Rows
update_histogram(df.loc[df["aboutCorona"]], "polarity", 3, "Corona Polarity")
update_histogram(df.loc[df["aboutCorona"]], "subjectivity", 4, "Corona Subjectivity")

# Resistance Rows
update_histogram(df.loc[df["aboutResistance"]], "polarity", 5, "Resistance Polarity")
update_histogram(df.loc[df["aboutResistance"]], "subjectivity", 6, "Resistance Subjectivity")

# Virus Rows
update_histogram(df.loc[df["aboutVirus"]], "polarity", 7, "Virus Polarity")
update_histogram(df.loc[df["aboutVirus"]], "subjectivity", 8, "Virus Subjectivity")

plt.show()
