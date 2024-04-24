+++
date = '2022-05-18T14:40:32'
description = 'Testing TensorFlow models against the SCDB data set.'
title = 'Conduct Legal Research with AI: Part 3'
featured_image = 'post-image.png'
author = "Justin Napolitano"
image = "post-image.*"
categories = ['Legal Research', 'Data Wrangling', 'Graph Database', 'Automation', 'Machine Learning', 'TensorFlow']
tags = ['python','legal', 'json', 'scotus', 'automation','machine-learning', 'ai', 'ml']
images = ['featured-justices.jpeg']
series = ['Legal Research with AI']
+++


# Conduct Legal Research with AI: Part 3

This is the third post in a series documenting the process of building an ml pipeline that will be used to train models to predict the outcomes of Supreme Court Cases.  

You can find the others at:

* [blog.jnapolitano.io/neo4j_integration/](https://blog.jnapolitano.io/neo4j_integration/)
* [blog.jnapolitano.io/constitution_to_neo/](https://blog.jnapolitano.io/constitution_to_neo/)

## Introduction

In this post, I will be testing a sample TensorFlow pipeline against the [Supreme Court Database](http://scdb.wustl.edu/) maintained by the Washington University Law School in order to build a proof of concept model for a Supreme Court Graph Analysis project. 


## The Data Set 

The data set is fairly limited. There are only about 250 issue areas to train against. It also does not include doctrinal trees to train an algorithm to predict when the court will break from precedent. 

The data records primarily the voting behavior of justices, the policy direction of the outcome, and the political ideology score of the outcome.  

Policy direction and political ideology are factors coded by individuals that may be prone to error an bias. In my analysis I will test against the findings of this model to determine which factors are most powerful.

## The Model

I tested against case centric and justice centric data orientations.  


### Case Centric Model

The first is case centric.  The power of this model is fairly limited, as it attempts to discern the outcome of a case from the aggregate behavior of the current justices on the bench.  It essentially creates a score that is modified by each case outcome to determine if the court will vote conservatively or liberally towards a case of regarding a specific issue area.  It is important to note that the database limits each case to one overarching issue area.  

#### Case Centric Training Features

* issue
* issueArea
* naturalCourt
* petitioner
* petitionerState
* respondent
* jurisdiction
* adminAction
* adminActionState
* threeJudgeFdc
* caseOrigin
* caseOriginState
* respondentState
* caseSource
* caseSourceState
* lawType
* lawSupp

#### Case Centric Results

The models were able to predict the outcomes about 75 percent of the time following 1,000 epochs of training.  It is likely that factors other than previous voting behavior determine the outcome of the case.  



### Justice Centric Model

The second is justice centric.  The predictive power of this model, should in theory be greater as it attempts to determine the likely vote of an individual justice against an issue area.  Again this is limited as only the overarching issue area is available in the data.  It may very well prove that justices may favor free speech in most cases, except when the military is the target.  The model could not predict that, because the data is limited.  

#### Justice Centric Training Features

* justice
* issue
* issueArea
* lawType
* direction
* petitioner
* naturalCourt
* petitionerState
* respondent
* respondentState
* jurisdiction
* caseOrigin
* caseOriginState
* caseSource
* caseSourceState
* certReason
* lawSupp

#### Justice Centric Results

The justice centric pipeline results in accuracy exceeding 82 percent.  This is better, but a model that could consider more factors and issue areas would likely improve the results.  


## Next Steps

I will integrate the models to my neo4j data set.  As of now, the graph database exceeds 50,000 individuals nodes and over 400,000 relationships.  It will allow me to train an algorithm that can determine a justices attitude towards, cases, clauses, sentences, states, petitioners, and any other feature integrated into the dataset.  


## The Code 

### Case Centric Training Pipeline 

I've included the entire model below.  Review my [documentation site](https://docs.jnapolitano.io/parts/ml-ai/tensorflow/project-supcourt-tensorflow/docs/SupremeCourtPredictionsCase/index.html) for more detail.   

``` Python
#supremeCourtPrediction.py
#a program that uses the segal and spaeth dataset to predict the outcomes of cases


import pandas as pd

import tensorflow as tf

import math

import seaborn as sns
import matplotlib.pyplot as plt

import shap
shap.initjs()

import os 
import csv
import datetime

from tensorflow import feature_column
from tensorflow.keras import layers
from sklearn.model_selection import train_test_split

from itertools import permutations 

import matplotlib.pyplot as plt



def get_environmental_variables():
    cwd = os.getcwd()
    log_dir = os.path.join(cwd,"logs/fit/") + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    return cwd, log_dir



def load_data(cwd):
    data_path = os.path.join(cwd,'data','citation.csv') 
    drop_path = os.path.join(cwd,'data','features','drop','drop.txt')
    #print(path)
    dataframe = pd.read_csv(data_path,encoding= 'unicode_escape')
    #print(dataframe.head())
    
    with open(drop_path) as fp:
        for cnt, line in enumerate(fp):
            #print("Dropping {} from dataframe".format(line))
            line = line.strip('\n')
            line = line.strip('\t')
            line = line.strip("'")

            dataframe.drop(line,axis=1,inplace=True)
    
    dataframe.fillna(0, inplace=True)
    print(dataframe)
    #dataframe.issue = dataframe.astype({'issue': 'str'})
    #dataframe[issue] = dataframe[issue].astype(str)
    #print(dataframe)
    #print(dataframe.head())
    return dataframe



def split_datframe(dataframe):
    train, test = train_test_split(dataframe, test_size=0.2)
    train, val = train_test_split(train, test_size=0.2)
    print(len(train), 'train examples')
    print(len(val), 'validation examples')
    print(len(test), 'test examples')
    return train, test, val


    # A utility method to create a tf.data dataset from a Pandas Dataframe

def df_to_dataset(dataframe, shuffle=True, batch_size=32):
    dataframe = dataframe.copy()
    labels = dataframe.pop('declarationUncon')
    ds = tf.data.Dataset.from_tensor_slices((dict(dataframe), labels))
    if shuffle:
        ds = ds.shuffle(buffer_size=len(dataframe))
    ds = ds.batch(batch_size)
    print(ds)
    return ds



def get_input_pipeline(train, test, val, batch_size=32, shuffle=True):
    train_ds = df_to_dataset(train, batch_size=batch_size)
    val_ds = df_to_dataset(val, shuffle=False, batch_size=batch_size)
    test_ds = df_to_dataset(test, shuffle=False, batch_size=batch_size)
    return train_ds, val_ds, test_ds



def get_feature_layer(cwd): #select the columns for analysis from dataset
    feature_path = os.path.join(cwd,'data','features','use','features.txt')
    dict_path = os.path.join(cwd,'data','features','use')
    feature_columns = []
    
    #embedded columns
    with open(feature_path) as fp:
        for cnt, line in enumerate(fp):
            #print("Adding {} to features".format(line))
            line = line.strip('\n')
            line = line.strip('\t')
            line = line.strip("'")

            print(cnt)   
            print(line)

            indicator = feature_column.numeric_column(line)
            
            #feature_column.categorical_column_with_vocabulary_file(
            #            key = line, vocabulary_file = os.path.join(dict_path,"{}.txt".format(line)), default_value=0)

            print(indicator)
            feature_columns.append(indicator)


            #feature_columns.append(feature_column.embedding_column(indicator, dimension=8))

    
    crossed_feature = feature_column.crossed_column(['issue', 'issueArea', 'naturalCourt'], hash_bucket_size=1000)
    crossed_feature = feature_column.indicator_column(crossed_feature)
    feature_columns.append(crossed_feature)


    crossed_feature = feature_column.crossed_column(['issue', 'naturalCourt'], hash_bucket_size=1000)
    crossed_feature = feature_column.indicator_column(crossed_feature)
    feature_columns.append(crossed_feature)

    crossed_feature = feature_column.crossed_column(['issueArea', 'naturalCourt'],hash_bucket_size=1000)
    crossed_feature = feature_column.indicator_column(crossed_feature)
    feature_columns.append(crossed_feature)
    
   # court_buckets = feature_column.bucketized_column(naturalCourt, boundaries=[18, 25, 30, 35, 40, 45, 50, 55, 60, 65])

    #print(feature_columns)
    feature_layer = tf.keras.layers.DenseFeatures(feature_columns)
    #for item in feature_columns:
    #    print(item)
    #    print("\n")

    return feature_layer

     
    #crossed cols


    #categorical_columns 

def understand_input_pipeline(train_ds):
    for feature_batch, label_batch in train_ds.take(1):
        print('Every feature:', list(feature_batch.keys()))
        #print('A batch of ages:', feature_batch['age'])
        print('A batch of targets:', label_batch )



def create_model(log_dir,feature_layer, train_ds, val_ds, epochs = 5):
    
    model = tf.keras.Sequential([
        feature_layer,
        layers.Dense(128, activation='relu'),
        layers.Dense(128, activation='relu'),
        layers.Dense(1)
    ])

    model.compile(optimizer='adam',
            loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
            metrics=['accuracy', 'mae'])

    history = model.fit(train_ds,
            validation_data=val_ds,
            epochs=epochs)

    loss, accuracy,mae = model.evaluate(test_ds)
    print("Accuracy", accuracy)
    print(model.summary())
    return model,history


def plot_history(history):

    hist = pd.DataFrame(history.history)
    print(hist)
    hist['epoch'] = history.epoch

    plt.figure()
    plt.xlabel('Epoch')
    plt.ylabel('Mean Absolute Error')
    plt.plot(hist['epoch'], hist['mae'],
            label='Train Error')
    plt.plot(hist['epoch'], hist['val_mae'],
            label = 'Val Error')
    plt.legend()



def explain_kernal(df_train,model,train_ds):
    
    # KernelExplainer is a general approach that can work with any ML framework
    # Its inputs are the predictions and training data

    # Summarize the training set to accelerate analysis
    df_train_summary = shap.kmeans(df_train.values, 25)

    # Instantiate an explainer with the model predictions and training data summary
    explainer = shap.KernelExplainer(model.predict, df_train)


# Extract Shapley values from the explainer
    #shap_values = explainer.shap_values(df_train.values)
if __name__ == "__main__":
    cwd, log_dir = get_environmental_variables()
    #print(cwd)

    df = load_data(cwd)

    train,test,val = split_datframe(df)
    dataset = df_to_dataset(df)
    train_ds, val_ds, test_ds = get_input_pipeline(train,test,val,32)
    understand_input_pipeline(train_ds)
    feature_layer = get_feature_layer(cwd)
    model, model_history = create_model(log_dir,feature_layer, train_ds, val_ds)
    plot_history(model_history)
    #print(model.predict(train_ds))
    #print(model.predict)
    explain_kernal(df,model,train_ds)
```

### The Justice Centric Training Pipeline

The entire pipeline is included below.  Review the [documentation](https://docs.jnapolitano.io/parts/ml-ai/tensorflow/project-supcourt-tensorflow/docs/SupremeCourtPredictionsJustice/index.html) for greater detail.


``` python
#supremeCourtPrediction.py
#a program that uses the segal and spaeth dataset to predict the outcomes of cases


import pandas as pd

import tensorflow as tf

import math

import seaborn as sns
import matplotlib.pyplot as plt

import shap
shap.initjs()

import os 
import csv
import datetime

from tensorflow import feature_column
from tensorflow.keras import layers
from sklearn.model_selection import train_test_split

from itertools import permutations
from itertools import combinations_with_replacement

import matplotlib.pyplot as plt




def get_environmental_variables():
    cwd = os.getcwd()
    log_dir = os.path.join(cwd,"logs/fit/") + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    return cwd, log_dir




def load_data(cwd):
    data_path = os.path.join(cwd,'data','justice.csv') 
    drop_path = os.path.join(cwd,'data','features','drop','drop.txt')
    target_path = os.path.join(cwd,'data','features','targets.txt')
    print(data_path)
    dataframe = pd.read_csv(data_path,encoding= 'unicode_escape')
    #print(dataframe.head())
    
    with open(drop_path) as fp:
        for cnt, line in enumerate(fp):
            #print("Dropping {} from dataframe".format(line))
            line = line.strip('\n')
            line = line.strip('\t')
            line = line.strip("'")

            dataframe.drop(line,axis=1,inplace=True)
    
    dataframe.fillna(0, inplace=True)
    print(dataframe)
    #dataframe.issue = dataframe.astype({'issue': 'str'})
    #dataframe[issue] = dataframe[issue].astype(str)
    #print(dataframe)
    #print(dataframe.head())
    return dataframe




def split_datframe(dataframe):
    train, test = train_test_split(dataframe, test_size=0.2)
    train, val = train_test_split(train, test_size=0.2)
    print(len(train), 'train examples')
    print(len(val), 'validation examples')
    print(len(test), 'test examples')
    return train, test, val


    # A utility method to create a tf.data dataset from a Pandas Dataframe


def df_to_dataset(dataframe, shuffle=True, batch_size=32):
    dataframe = dataframe.copy()
    labels = dataframe.pop('vote')
    ds = tf.data.Dataset.from_tensor_slices((dict(dataframe), labels))
    if shuffle:
        ds = ds.shuffle(buffer_size=len(dataframe))
    ds = ds.batch(batch_size)
    print(ds)
    return ds




def get_input_pipeline(train, test, val, batch_size=32, shuffle=True):
    train_ds = df_to_dataset(train, batch_size=batch_size)
    val_ds = df_to_dataset(val, shuffle=False, batch_size=batch_size)
    test_ds = df_to_dataset(test, shuffle=False, batch_size=batch_size)
    return train_ds, val_ds, test_ds




def get_feature_layer(cwd): #select the columns for analysis from dataset
    feature_path = os.path.join(cwd,'data','features','use','features.txt')
    dict_path = os.path.join(cwd,'data','features','use')
    feature_columns = []
    feature_list = []
    #embedded columns
    with open(feature_path) as fp:
        for cnt, line in enumerate(fp):
            #print("Adding {} to features".format(line))
            line = line.strip('\n')
            line = line.strip('\t')
            line = line.strip("'")

            print(cnt)   
            print(line)
            feature_list.append(line)

            indicator = feature_column.numeric_column(line)
            
            #feature_column.categorical_column_with_vocabulary_file(
            #            key = line, vocabulary_file = os.path.join(dict_path,"{}.txt".format(line)), default_value=0)

            print(indicator)
            feature_columns.append(indicator)


            #feature_columns.append(feature_column.embedding_column(indicator, dimension=8))

    feature_comb = combinations_with_replacement(feature_list, 2) 
    lst = list(feature_comb)
    limit = len(feature_list)
    print(limit)
    j = 0
    k = limit - 1
    lookup = []
    for i in range(limit):
        lookup.append(i+j)
        j = j + k
        k = k - 1 


    for i in range(len(lst)):
        if i in lookup:
            continue
        else:
            one, two = lst[i]
            crossed_feature = feature_column.crossed_column([one, two], hash_bucket_size=1000)
            crossed_feature = feature_column.indicator_column(crossed_feature)
            feature_columns.append(crossed_feature)

    """
    crossed_feature = feature_column.crossed_column(['issue', 'naturalCourt'], hash_bucket_size=1000)
    crossed_feature = feature_column.indicator_column(crossed_feature)
    feature_columns.append(crossed_feature)

    crossed_feature = feature_column.crossed_column(['issueArea', 'naturalCourt'],hash_bucket_size=1000)
    crossed_feature = feature_column.indicator_column(crossed_feature)
    feature_columns.append(crossed_feature)
    """
   # court_buckets = feature_column.bucketized_column(naturalCourt, boundaries=[18, 25, 30, 35, 40, 45, 50, 55, 60, 65])

    #print(feature_columns)
    feature_layer = tf.keras.layers.DenseFeatures(feature_columns)
    #for item in feature_columns:
    #    print(item)
    #    print("\n")

    return feature_layer

     
    #crossed cols


    #categorical_columns 


def understand_input_pipeline(train_ds):
    for feature_batch, label_batch in train_ds.take(1):
        print('Every feature:', list(feature_batch.keys()))
        #print('A batch of ages:', feature_batch['age'])
        print('A batch of targets:', label_batch )




def create_model(log_dir,feature_layer, train_ds, val_ds, epochs = 8):
    
    model = tf.keras.Sequential([
        feature_layer,
        layers.Dense(128, activation='relu'),
        layers.Dense(128, activation='relu'),
        layers.Dense(1)
    ])

    model.compile(optimizer='adam',
            loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
            metrics=['accuracy', 'mae'])

    history = model.fit(train_ds,
            validation_data=val_ds,
            epochs=epochs)

    loss, accuracy,mae = model.evaluate(test_ds)
    print("Accuracy", accuracy)
    print(model.summary())
    return model,history




def plot_history(history):

    hist = pd.DataFrame(history.history)
    print(hist)
    hist['epoch'] = history.epoch

    plt.figure()
    plt.xlabel('Epoch')
    plt.ylabel('Mean Absolute Error')
    plt.plot(hist['epoch'], hist['mae'],
            label='Train Error')
    plt.plot(hist['epoch'], hist['val_mae'],
            label = 'Val Error')
    plt.legend()




def explain_kernal(model,train_ds):
    model.predict(train_ds)
    # KernelExplainer is a general approach that can work with any ML framework
    # Its inputs are the predictions and training data

    # Summarize the training set to accelerate analysis
    df_train_summary = shap.kmeans(train_ds.values, 25)
    #print(df_train_summary)
    #model.predict(df_train_summary)
    # Instantiate an explainer with the model predictions and training data summary
    explainer = shap.KernelExplainer(model.predict, train_ds)


# Extract Shapley values from the explainer
    #shap_values = explainer.shap_values(df_train.values)
if __name__ == "__main__":
    cwd, log_dir = get_environmental_variables()
    print(cwd)


    df = load_data(cwd)

    train,test,val = split_datframe(df)
    dataset = df_to_dataset(df)
    train_ds, val_ds, test_ds = get_input_pipeline(train,test,val,32)
    understand_input_pipeline(train_ds)
    feature_layer = get_feature_layer(cwd)
    model, model_history = create_model(log_dir,feature_layer, train_ds, val_ds)
    #plot_history(model_history)
    #print(model.predict(train_ds))
    #print(model.predict)
    #explain_kernal(model,train_ds)
```





