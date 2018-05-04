from __future__ import absolute_import, print_function

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json

from textblob import TextBlob 
import matplotlib.pyplot as plt 
import re
import time



ACCESS_TOKEN = "126217834-djfopyZXriz5q32ByIsM0dBCUY2UYzAW2eiG1nKh"
ACCESS_SECRET = "5AvtTgeLoJNdbw5BwUO7ppqxBSJldY4bWPCanrpdPb14W" 
CONSUMER_KEY = "ZqcfoMt9YxIrBLZYP28qtdRxL"
CONSUMER_SECRET = "ctiHPBa0cW2X2BTG4kJPUf3hWbFHxo8Te1dCy65KUjs7cA1hLo"

# Go to http://apps.twitter.com and create an app.
# The consumer key and secret will be generated for you after
consumer_key=CONSUMER_KEY
consumer_secret=CONSUMER_SECRET

# After the step above, you will be redirected to your app's page.
# Create an access token under the the "Your access token" section
access_token=ACCESS_TOKEN
access_token_secret=ACCESS_SECRET


positive = 0
negative = 0
compound = 0

count = 0
init_time = time.time()
plt.ion()

def calctime(a):
    return time.time()-a




# class StdOutListener(StreamListener):
#     """ A listener handles tweets that are received from the stream.
#     This is a basic listener that just prints received tweets to stdout.
#     """
#     def on_data(self, data):
#         print(data)
#         return True

#     def on_error(self, status):
#         print(status)


class listener(StreamListener):
    def on_data(self, data):
        
        global init_time
        t = int(calctime(init_time))
        
        all_data = json.loads(data)
        tweet = all_data["text"].encode("utf-8")

        tweet = " ".join(re.findall("[a-zA-Z]+", tweet.decode("utf-8")))
        blob = TextBlob(tweet.strip())

        global positive
        global negative
        global compound
        global count


        count = count + 1
        senti = 0

        for sen in blob.sentences:
            senti = senti + sen.sentiment.polarity

            if sen.sentiment.polarity >= 0:
                positive = positive + sen.sentiment.polarity
            else:
                 negative = negative + sen.sentiment.polarity

            compound = compound + senti 

            print(count)
            print(tweet.strip())
            print(senti)
            print(t)
            print( str(positive) +" "+ str(negative)+" "+str(compound))

            plt.axis([0,70,-20,20])
            plt.xlabel("Time")
            plt.ylabel("Sentiment")
            plt.plot([t], [senti],"-")
            # plt.plot([t], [positive], " go ", [t], [negative], 'ro',[t],[compound],'bo')
            plt.show()

            plt.pause(0.0001)

            if count == 200:
                return False
            else:
                return True




    def on_error(self, status):
        print(status)

if __name__ == '__main__':
    listen = listener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, listen)
    stream.filter(track=['Avengers: Infinity War'])
