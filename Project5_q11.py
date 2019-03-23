import json
import pytz
import datetime
import time
import pandas as pd
import winsound
import numpy as np
import matplotlib.pyplot as plt
from math import sqrt
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import KFold
from sklearn.pipeline import Pipeline
from tempfile import mkdtemp
from shutil import rmtree
from Project5_q6 import feature_extraction, min_max_timestamps
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPRegressor
from sklearn.externals.joblib import Memory
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from pandas import ExcelWriter
from pandas import DataFrame, read_csv


pst_tz = pytz.timezone('America/Los_Angeles')


frequency = 2500  # Set Frequency To 2500 Hertz
duration = 1000  # Set Duration To 1000 ms == 1 second

s = 'file_aggreg.txt'
l = min_max_timestamps(s)

beginstamp = l[0]
endstamp = l[1]

stamp1 = int(time.mktime(datetime.datetime(2015, 2, 1, 8, 0, 0, 0, pst_tz).timetuple()))
stamp2 = int(time.mktime(datetime.datetime(2015, 2, 1, 20, 0, 0, 0, pst_tz).timetuple()))

features = feature_extraction(beginstamp,endstamp,3600,s)


param_grid = {
'hidden_layer_sizes': [(10,5),(20,5),(30,5),(1000,20),(500,10)]
}

mlpr = MLPRegressor()
grid_search = GridSearchCV( estimator = mlpr, param_grid = param_grid,
                            cv=KFold(5, shuffle=True), n_jobs=-1,verbose = 2,scoring='neg_mean_squared_error')

dk1 = features.values



grid_search.fit(dk1[:,:-1], dk1[:,-1])

print(grid_search.best_params_)

df = pd.DataFrame(grid_search.cv_results_)

# Create a Pandas Excel writer using XlsxWriter as the engine.
writer = pd.ExcelWriter('q11.xlsx', engine='xlsxwriter')

# Convert the dataframe to an XlsxWriter Excel object.
df.to_excel(writer, sheet_name='Sheet1')

# Close the Pandas Excel writer and output the Excel file.
writer.save()

winsound.Beep(frequency, duration)



