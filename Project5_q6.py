import json
import pytz
import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from math import sqrt
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score



pst_tz = pytz.timezone('America/Los_Angeles')

mincit = 10e9
maxcit = -1


with open("ECE219_tweet_data/tweets_#gopatriots.txt",encoding="utf-8") as f:
    for line in f:
        # print(line)
        json_object = json.loads(line)
        #
        # l1.append(json_object['metrics']['citations']['total'])
        # ln.append(json_object['original_author']['followers'])
        # lt.append(json_object['citation_date'])
        # la.append(json_object['author'])

        if json_object['citation_date'] <mincit:
            mincit = json_object['citation_date']
        if json_object['citation_date'] >maxcit:
            maxcit = json_object['citation_date']




beginstamp = mincit
beginstamp -= beginstamp % 3600
print(beginstamp)

endstamp = maxcit
endstamp -= endstamp % 3600
print(endstamp)



##################### adjustment for range function ######################3
endstamp = endstamp + 3600

print((endstamp-beginstamp)/3600)

number_of_tweets = [0 for stamp in range(beginstamp,endstamp,3600)]
number_of_retweets = [0 for stamp in range(beginstamp,endstamp,3600)]
s_number_of_followers = [0 for stamp in range(beginstamp,endstamp,3600)]
max_of_followers = [0 for stamp in range(beginstamp,endstamp,3600)]
time_of_day = [0 for stamp in range(beginstamp,endstamp,3600)]
target = [0 for stamp in range(beginstamp,endstamp,3600)]

for idx, stamp in enumerate(range(beginstamp,endstamp,3600)):
    time_of_day[idx] = datetime.datetime.fromtimestamp(stamp, pst_tz).hour


with open("ECE219_tweet_data/tweets_#gopatriots.txt", encoding="utf-8") as f:
    for line in f:
        # print(line)
        json_object = json.loads(line)
        stamp =  json_object['citation_date']
        stamp -= stamp % 3600
        idx = int((stamp-beginstamp)/3600)
        number_of_tweets[idx] += 1
        number_of_retweets[idx] += json_object['metrics']['citations']['total']
        s_number_of_followers[idx] += json_object['author']['followers']
        max_of_followers[idx] = max(max_of_followers[idx],json_object['author']['followers'])
        if idx >0:
            target[idx-1] += 1

print('-'*40)

print(target)
print(len(time_of_day))






# print(datetime.datetime.fromtimestamp(timestamp, pst_tz))
#
# min_pst_time = datetime.datetime.fromtimestamp(mincit, pst_tz)
# #############################  set minutes, seconds and microseconds to zero #############
# t = min_pst_time.replace(minute=0, second=0, microsecond=0)
# print(t)

#
# for idx,i in enumerate(l1[45:48]):
#     print(i)
#     print()
#     print(ln[idx+45])
#     print()
#     print(la[idx+45])
#     print()
#     ################################   for hours ###################################
#     print(datetime.datetime.fromtimestamp(lt[idx+45], pst_tz).hour)
#     ##################################################################################
#     print('-'*40)
#     print()
# print(mincit)
# print(mincit+3600)
# print(datetime.datetime.fromtimestamp(mincit, pst_tz))
# print(datetime.datetime.fromtimestamp(mincit+3600, pst_tz))
# print()
# print((maxcit-mincit)/3600)
# print(datetime.datetime.fromtimestamp(maxcit, pst_tz))

#
#
#















# for i in ln[45:48]:
#     print(i)
#
# print()

# l2 = []
# with open("ECE219_tweet_data/tweets_#sb49.txt", encoding="utf-8") as f:
#     for line in f:
#         # print(line)
#         json_object = json.loads(line)
#         l2.append(json_object['citation_date'])
#
# for i in l2[45:48]:
#     print(i)
#
# print()
#
# l3 = []
# with open("ECE219_tweet_data/tweets_#superbowl.txt", encoding="utf-8") as f:
#     for line in f:
#         # print(line)
#         json_object = json.loads(line)
#         l3.append(json_object['citation_date'])
#
# for i in l3[5:48]:
#     print(i)
#
# print()
#
# l4 = []
# with open("ECE219_tweet_data/tweets_#nfl.txt", encoding="utf-8") as f:
#     for line in f:
#         # print(line)
#         json_object = json.loads(line)
#         l4.append(json_object['citation_date'])
#
# for i in l4[45:48]:
#     print(i)
#
# print()
#
# l5 = []
# with open("ECE219_tweet_data/tweets_#patriots.txt", encoding="utf-8") as f:
#     for line in f:
#         # print(line)
#         json_object = json.loads(line)
#         l5.append(json_object['citation_date'])
#
# for i in l5[45:48]:
#     print(i)
#
# print()
#
# l6 = []
# with open("ECE219_tweet_data/tweets_#gohawks.txt", encoding="utf-8") as f:
#     for line in f:
#         # print(line)
#         json_object = json.loads(line)
#         l6.append(json_object['citation_date'])
#
# for i in l6[45:48]:
#     print(i)
#
# print()