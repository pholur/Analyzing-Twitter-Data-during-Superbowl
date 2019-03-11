import json
import pytz
import datetime
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from math import sqrt
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score



pst_tz = pytz.timezone('America/Los_Angeles')

def min_max_timestamps(s):
    mincit = 10e9
    maxcit = -1

    with open(s, encoding="utf-8") as f:
        for line in f:
            json_object = json.loads(line)
            if json_object['citation_date'] < mincit:
                mincit = json_object['citation_date']
            if json_object['citation_date'] > maxcit:
                maxcit = json_object['citation_date']
    return [mincit,maxcit]


def feature_extraction(beginstamp, endstamp, window,s):
    #############  Preprocessing #############
    beginstamp -= beginstamp % window
    endstamp -= endstamp % window
    #########################################
    number_of_tweets = [0 for stamp in range(beginstamp, endstamp, window)]
    number_of_retweets = [0 for stamp in range(beginstamp, endstamp, window)]
    s_number_of_followers = [0 for stamp in range(beginstamp, endstamp, window)]
    max_of_followers = [0 for stamp in range(beginstamp, endstamp, window)]
    time_of_day = [0 for stamp in range(beginstamp, endstamp, window)]
    target = [0 for stamp in range(beginstamp, endstamp, window)]

    for idx, stamp in enumerate(range(beginstamp, endstamp, window)):
        time_of_day[idx] = datetime.datetime.fromtimestamp(stamp, pst_tz).hour

    limit = int((endstamp - beginstamp) / window)

    with open(s, encoding="utf-8") as f:
        for line in f:
            # print(line)
            json_object = json.loads(line)
            stamp = json_object['citation_date']
            stamp -= stamp % window
            idx = int((stamp - beginstamp) / window)

            if idx < limit and idx >=0:

                number_of_tweets[idx] += 1
                number_of_retweets[idx] += json_object['metrics']['citations']['total']
                s_number_of_followers[idx] += json_object['author']['followers']
                max_of_followers[idx] = max(max_of_followers[idx], json_object['author']['followers'])
            if idx > 0 and idx <=limit:

                target[idx - 1] += 1


    feature_target = pd.DataFrame(
        {'number_of_tweets': number_of_tweets,
         'number_of_retweets': number_of_retweets,
         's_number_of_followers': s_number_of_followers,
         'max_of_followers': max_of_followers,
         'time_of_day': time_of_day,
         'target': target
         })
    return feature_target



def lin_regress_r(datum):
    reg_fin = LinearRegression().fit(datum[:,:-1], datum[:,-1])
    pred = reg_fin.predict(datum[:,:-1])
    rmse_trn = (mean_squared_error(datum[:, -1], pred))
    return rmse_trn


s = 'ECE219_tweet_data/tweets_#superbowl.txt'
l = min_max_timestamps(s)

beginstamp = l[0]
endstamp = l[1]

# v = datetime.datetime.fromtimestamp(beginstamp, pst_tz)
# print(v)
# time1 = int(time.mktime(datetime.datetime(v.year, v.month, v.day, v.hour, v.minute, v.second, v.microsecond, pst_tz).timetuple()))

features = feature_extraction(beginstamp,endstamp,3600,s)


stamp1 = int(time.mktime(datetime.datetime(2015, 2, 1, 8, 0, 0, 0, pst_tz).timetuple()))
stamp2 = int(time.mktime(datetime.datetime(2015, 2, 1, 20, 0, 0, 0, pst_tz).timetuple()))

feature1 = feature_extraction(beginstamp,stamp1,3600,s)
feature2 = feature_extraction(stamp1,stamp2,300,s)
feature3 = feature_extraction(stamp2,endstamp,3600,s)

dk1 = feature1.values
print(lin_regress_r(dk1))
print()
dk2 = feature2.values
print(lin_regress_r(dk2))
print()
dk3 = feature3.values
print(lin_regress_r(dk3))
print()





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
# for i in ln[45:48]:
#     print(i)
#
# print()
