import json
import pytz
import datetime
import pandas as pd
import numpy as np

def extract_feat(file_name):

    pst_tz = pytz.timezone('America/Los_Angeles')
    # to find the time of first and last post in the set
    mincit = 10e9
    maxcit = -1


    with open(file_name,encoding="utf-8") as f:
        for line in f:
            json_object = json.loads(line)
            if json_object['citation_date'] < mincit:
                mincit = json_object['citation_date']
            if json_object['citation_date'] > maxcit:
                maxcit = json_object['citation_date']
    # found the time of first and last post (absolute time)


    # rounding the beginstamp to the correct full first dataset
    # legit features must be rich in features (begin) AND target (end)

    beginstamp = mincit
    if beginstamp % 3600 == 0:
        beginstamp = beginstamp
    else:
        beginstamp -= beginstamp % 3600
        beginstamp = beginstamp + 3600
        feat_begin_hr = int(beginstamp / 3600)


    endstamp = maxcit
    if endstamp % 3600 == 0:
        endstamp = endstamp - 3600
    else:
        endstamp -= endstamp % 3600
        endstamp = endstamp - 3600
        feat_end_hr = int(endstamp / 3600)


    #print((endstamp-beginstamp)/3600)

    #initialize the VARs
    number_of_tweets = [0 for stamp in range(feat_begin_hr,feat_end_hr)]
    number_of_retweets = [0 for stamp in range(feat_begin_hr,feat_end_hr)]
    s_number_of_followers = [0 for stamp in range(feat_begin_hr,feat_end_hr)]
    max_of_followers = [0 for stamp in range(feat_begin_hr,feat_end_hr)]
    time_of_day = [0 for stamp in range(feat_begin_hr,feat_end_hr)]
    target = [0 for stamp in range(feat_begin_hr,feat_end_hr)]

    for idx, stamp in enumerate(range(beginstamp,endstamp,3600)):
        time_of_day[idx] = datetime.datetime.fromtimestamp(stamp, pst_tz).hour


    with open(file_name, encoding="utf-8") as f:
        for line in f:
            # print(line)
            json_object = json.loads(line)
            stamp = json_object['citation_date']
            stamp -= stamp % 3600
            idx = int((stamp-beginstamp)/3600)
            #print(idx)

            if idx < feat_end_hr - feat_begin_hr:
                number_of_tweets[idx] += 1
                number_of_retweets[idx] += json_object['metrics']['citations']['total']
                s_number_of_followers[idx] += json_object['author']['followers']
                max_of_followers[idx] = max(max_of_followers[idx],json_object['author']['followers'])

            if idx > 0 and idx < feat_end_hr - feat_begin_hr + 1:
                    target[idx-1] += 1

    table = [number_of_tweets, number_of_retweets, s_number_of_followers, max_of_followers, time_of_day, target]
    df = pd.DataFrame(table)
    df = df.transpose()
    df.columns= ['N','NR','SNF','MF','TD','target']
    # print(df)
    return df

if __name__ == '__main__':
    tweet_gohawks = extract_feat("tweets_#gohawks.txt")


