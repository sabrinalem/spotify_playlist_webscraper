import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from sklearn import preprocessing
from sklearn.model_selection import KFold
from sklearn.linear_model import LinearRegression
import json
import os

# Directory
def directoryList():
    directory = "/Users/sabrinalem/Desktop/FriData_Functions/data"
    x =  os.listdir(directory)
    x.remove('date')
    x.remove('.DS_Store')
    return x
directory = directoryList()

# iterate through directory and get list of all files in folder data
list = []
for x in directory:
    get = f"/Users/sabrinalem/Desktop/FriData_Functions/data/{x}/summary.csv"
    list.append(get)

# get sample means of all variables 
danceability_means = []
for y in range(len(list)):
    dir = list[y]
    summary = pd.read_csv(dir)
    danceability_means.append(summary['danceability'][0].copy())
print(danceability_means)
energy_means = []
for y in range(len(list)):
    dir = list[y]
    summary = pd.read_csv(dir)
    energy_means.append(summary['energy'][0].copy())
key_means = []
for y in range(len(list)):
    dir = list[y]
    summary = pd.read_csv(dir)
    key_means.append(summary['key'][0].copy())
loudness_means = []
for y in range(len(list)):
    dir = list[y]
    summary = pd.read_csv(dir)
    loudness_means.append(summary['loudness'][0].copy())
mode_means = []
for y in range(len(list)):
    dir = list[y]
    summary = pd.read_csv(dir)
    mode_means.append(summary['mode'][0].copy())
speechiness_means = []
for y in range(len(list)):
    dir = list[y]
    summary = pd.read_csv(dir)
    speechiness_means.append(summary['speechiness'][0].copy())
acousticness_means = []
for y in range(len(list)):
    dir = list[y]
    summary = pd.read_csv(dir)
    acousticness_means.append(summary['acousticness'][0].copy())
instrumentalness_means = []
for y in range(len(list)):
    dir = list[y]
    summary = pd.read_csv(dir)
    instrumentalness_means.append(summary['instrumentalness'][0].copy())
liveness_means = []
for y in range(len(list)):
    dir = list[y]
    summary = pd.read_csv(dir)
    liveness_means.append(summary['liveness'][0].copy())
valence_means = []
for y in range(len(list)):
    dir = list[y]
    summary = pd.read_csv(dir)
    valence_means.append(summary['valence'][0].copy())
tempo_means = []
for y in range(len(list)):
    dir = list[y]
    summary = pd.read_csv(dir)
    tempo_means.append(summary['tempo'][0].copy())
duration_ms_means = []
for y in range(len(list)):
    dir = list[y]
    summary = pd.read_csv(dir)
    duration_ms_means.append(summary['duration_ms'][0].copy())
time_signature_means = []
for y in range(len(list)):
    dir = list[y]
    summary = pd.read_csv(dir)
    time_signature_means.append(summary['time_signature'][0].copy())








#getting Weekly Data
aftTable = pd.read_csv("/Users/sabrinalem/Desktop/FriData_Functions/data/21-08-20/aftTable.csv")
summary = pd.read_csv("/Users/sabrinalem/Desktop/FriData_Functions/data/21-09-17/summary.csv")
with open("/Users/sabrinalem/Desktop/FriData_Functions/data/21-09-17/specs.json") as file:
    specs = json.load(file)


# Average Artist Popularity for a given week 
def avgPop(specs):
    l = []
    for k in specs:
        artPop = specs[k]['artistPop']
        x = sum(artPop)
        y = len(artPop)
        avg = x/y
        l.append(avg)
    return l

# Audio Feature Correlation Graph
def graph(aftTable, varX, varY):
    fig = fig=plt.figure()
    ax = fig.add_subplot(1,1,1)
    varA = aftTable[varX]
    varB = aftTable[varY]
    ax.scatter(varA, varB)
    plt.title("%s x %s"%(varX, varY))
    plt.xlabel(varX)
    plt.ylabel(varY)
    return plt.show()


#graph(aftTable, 'danceability' , 'energy')







