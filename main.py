import tweepy
from textblob import TextBlob
from tweepy.streaming import StreamListener
import time
import csv
import collections
import pandas as pd
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt




API_KEY ='Jmuu7yvhrH8DB76925hM7hzKl'
API_SECRET_KEY='tYv5B1RgAcWhCohvXd93ythU3vsRHMz0mL69edFx9sGCI6bNtL'

ACCESS_TOKEN ='2453645750-lGnVHjWifrmVUaI6pSHy96f7uDcQmqSCNwPpzZr'
ACCESS_TOKEN_SECRET = 'xnRu1zRm2uUP5p6NSsumQ4VSQnQthqjuOtYcyfmfPlDb8'

auth = tweepy.OAuthHandler(API_KEY,API_SECRET_KEY)
auth.set_access_token(ACCESS_TOKEN,ACCESS_TOKEN_SECRET)

api =tweepy.API(auth)

test = api.search('test')

collection = {}
class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        text = status.text
        print(text)
        temp = TextBlob(text)
        temp = temp.lower()
        for word in temp.words:
            if word in collection:
                collection[word] += 1
            else:
                collection[word] = 1

def load_blacklist():
    black_list = []
    with open('black_list.csv', "r") as f:
        reader = csv.reader(f)
        for line in reader:
            tmp = line[0]
            black_list.append(tmp)
    return black_list

#init
black_list = load_blacklist()
myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=MyStreamListener())

try:
    myStream.filter(track=["test"],languages=['en'])
except KeyboardInterrupt:
    print("ende")

df_collection = pd.DataFrame.from_dict(collection,orient='index')
df_collection.columns = ['count']
df_collection = df_collection.sort_values(by='count',ascending=False)
for index,row in df_collection.iterrows():
    for black_listed in black_list:
        if black_listed == index:
            print('deleted  ',black_listed)
            df_collection.drop(index, inplace=True)

i = 0
data = []
count_list = []
for index,row in df_collection.iterrows():
    data.append(index)
    count_list.append(row['count'])
    i += 1
    if i > 10:
        break

print(data)


#mathplotlib visualisation
y_pos = np.arange(len(data))
plt.bar(y_pos, count_list,align='center', alpha=0.5)
plt.xticks(y_pos, data)
plt.ylabel('Usage')
plt.title('most used twitter word for sport topics' )
plt.show()

df_collection.to_csv('data_twitter.csv',sep="\t")

