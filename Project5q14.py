import json
import pytz
import datetime
import time
import winsound
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from math import sqrt
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import KFold
import statsmodels.api as sm
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
    # if beginstamp % window == 0:
    #     beginstamp = beginstamp
    # else:
    #     beginstamp -= beginstamp % window
    #     beginstamp = beginstamp + window
    beginstamp -= beginstamp % window

    endstamp -= endstamp % window
    #########################################
    number_of_tweets = [0 for stamp in range(beginstamp, endstamp, window)]
    number_of_retweets = [0 for stamp in range(beginstamp, endstamp, window)]
    s_number_of_followers = [0 for stamp in range(beginstamp, endstamp, window)]
    max_of_followers = [0 for stamp in range(beginstamp, endstamp, window)]
    time_of_day = [0 for stamp in range(beginstamp, endstamp, window)]
    listed_count = [0 for stamp in range(beginstamp, endstamp, window)]
    s_foll_of_orig_auth = [0 for stamp in range(beginstamp, endstamp, window)]
    ranking_score = [0 for stamp in range(beginstamp, endstamp, window)]
    num = 0
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
                num +=1
                number_of_retweets[idx] += json_object['metrics']['citations']['total']
                s_number_of_followers[idx] += json_object['author']['followers']
                max_of_followers[idx] = max(max_of_followers[idx], json_object['author']['followers'])
                hehe = json_object['tweet']['user']['listed_count']
                listed_count[idx] += hehe if hehe != None else 0
                s_foll_of_orig_auth[idx] += json_object['original_author']['followers']
                ranking_score[idx] += json_object['metrics']['ranking_score']
            if idx > 0 and idx <=limit:

                target[idx - 1] += 1
    # print(s)
    # print(num)
    feature_target = pd.DataFrame(
        {'number_of_tweets': number_of_tweets,
         'number_of_retweets': number_of_retweets,

         'listed_count': listed_count,
         's_foll_of_orig_auth': s_foll_of_orig_auth,
         'ranking_score': ranking_score,
         'target': target
         })
    return feature_target



def lin_regress_r(datum,testname,testwindow):


    reg_fin = LinearRegression().fit(datum[:,:-1], datum[:,-1])
    pred = reg_fin.predict(datum[:,:-1])
    rmse_trn = (mean_squared_error(datum[:, -1], pred))


    ################################  testing ##########################################################

    l = min_max_timestamps(testname)

    beginstamptest = l[0]
    endstamptest = l[1]
    testfeatures = feature_extraction(beginstamptest,endstamptest,testwindow,testname)
    testdata = testfeatures.values
    testpred = reg_fin.predict(testdata[:, :-1])
    print('number of tweets')
    print(testdata[:,1])
    print('Predicitions')
    print(testpred)
    # print('actual values')
    # print(testdata[:, -1])
    # print()
    # print(testfeatures)
    testrmse = (mean_squared_error(testdata[:, -1], testpred))


    return [rmse_trn,testrmse]







if __name__ == '__main__':
    #names = ["tweets_#gohawks.txt", "tweets_#gopatriots.txt","tweets_#nfl.txt", "tweets_#patriots.txt", "tweets_#sb49.txt", "tweets_#superbowl.txt"]
    names = ['file_aggreg.txt']
    frequency = 2500  # Set Frequency To 2500 Hertz
    duration = 2000  # Set Duration To 1000 ms == 1 second
    testnames = ['sample0_period1.txt','sample0_period2.txt','sample0_period3.txt','sample1_period1.txt','sample1_period2.txt','sample1_period3.txt','sample2_period1.txt','sample2_period2.txt','sample2_period3.txt']
    # s = 'ECE219_tweet_data/tweets_#gopatriots.txt'
    # s_write = 'tweets_#gopatriots.xlsx'
    for s in names:
        l = min_max_timestamps(s)

        beginstamp = l[0]
        endstamp = l[1]



        stamp1 = int(time.mktime(datetime.datetime(2015, 2, 1, 8, 0, 0, 0, pst_tz).timetuple()))
        stamp2 = int(time.mktime(datetime.datetime(2015, 2, 1, 20, 0, 0, 0, pst_tz).timetuple()))


        feature1 = feature_extraction(beginstamp,stamp1,3600,s)
        feature2 = feature_extraction(stamp1,stamp2,300,s)
        feature3 = feature_extraction(stamp2,endstamp,3600,s)
        name = ['MSE score','R-squared score','Train MSE','Test MSE']
        dk1 = feature1.values
        win1 = lin_regress_r(dk1,testnames[0],3600)
        print(testnames[0])
        dk2 = feature2.values
        win2 = lin_regress_r(dk2,testnames[1],300)
        print(testnames[1])
        dk3 = feature3.values
        win3 = lin_regress_r(dk3,testnames[2],3600)
        print(testnames[2])
        print(win1)
        print()
        print(win2)
        print()
        print(win3)
        winsound.Beep(frequency, duration)
