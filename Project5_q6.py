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



l1 = []
ln = []
lt = []

########################### element with mintimestamp
mincit = 10e9
########################## element with max timestamp
maxcit = -1


with open("ECE219_tweet_data/tweets_#gopatriots.txt",encoding="utf-8") as f:
    for line in f:
        # print(line)
        json_object = json.loads(line)

        l1.append(json_object['metrics']['citations']['total'])
        ln.append(json_object['original_author']['followers'])
        lt.append(json_object['citation_date'])
        if json_object['citation_date'] <mincit:
            mincit = json_object['citation_date']
        if json_object['citation_date'] >maxcit:
            maxcit = json_object['citation_date']


pst_tz = pytz.timezone('America/Los_Angeles')

####################### round off to the latest hour ##################
timestamp = mincit
timestamp -= timestamp % 3600
print(datetime.datetime.fromtimestamp(mincit, pst_tz))
print(datetime.datetime.fromtimestamp(timestamp, pst_tz))



##########################################################################
min_pst_time = datetime.datetime.fromtimestamp(mincit, pst_tz)
#############################  set minutes, seconds and microseconds to zero #############
t = min_pst_time.replace(minute=0, second=0, microsecond=0)
print(t)


for idx,i in enumerate(l1[45:48]):
    print(i)
    print()
    print(ln[idx+45])
    print()
    ################################   for hours ###################################
    print(datetime.datetime.fromtimestamp(lt[idx+45], pst_tz).hour)
    ##################################################################################
    print('-'*40)
    print()
print(mincit)
print(mincit+3600)
print(datetime.datetime.fromtimestamp(mincit, pst_tz))
print(datetime.datetime.fromtimestamp(mincit+3600, pst_tz))
print()
print((maxcit-mincit)/3600)
print(datetime.datetime.fromtimestamp(maxcit, pst_tz))

