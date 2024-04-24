+++
title =  "Conduct Legal Research with AI: Part 2"
date = "2022-05-17T18:40:32.169Z"
description = "Documenting classes and an application to integrate the US Constitution into my Neo4j DB"
author = "Justin Napolitano"
image = "post-image.png"
featuredimage = "post-image.png"
categories = ['Legal Research', 'Data Wrangling', 'Graph Database', 'Automation']
tags = ['python','legal', 'json', 'scotus', 'automation', 'neo4j']
images = ['featured-justices.jpeg']
series = ['Legal Research with AI']
+++

# Integrating the Constitution to Neo4j

I am currenlty building a graph database of Supreme Court cases in neo4j to model the behavior and decison making of the court.  

In this post, I include the classes that I will be using to create individual nodes for the articles, sections, clauses, and subclauses of the Consititution.  

Later, these will be related to cases and subjecst in order to train a tensorflow algorithm to recommend case law by issue area and to predict the outcome of cases.  


## Workflow 

The basic workflow requires creating a node and then submitting it to the neo4j db.   My previous posts have documented this process in detail.  Review [blog.jnapolitano.io/neo4j_integration/](https://blog.jnapolitano.io/neo4j_integration/) for more information.  

## Neomodel Api Classes

The neomodel classes below generate the nodes to be integrated into the database.  


### Article Class

``` python
class Article(StructuredNode):
    uuid = UniqueIdProperty()
    name = StringProperty(unique_index=True, required=True)
    topic = StringProperty(unique_index=True, required=True)
    citation = StringProperty(unique_index=True, required=True)
    clause = Relationship("Clause", "IS_ARTICLE_OF")
    sub_clause = Relationship("Subclause", "IS_ARTICLE_OF")
    case = Relationship("Case", 'IS_ARTICLE_OF')

```

### Section Class

``` python
class Section(StructuredNode):
    uuid = UniqueIdProperty()
    name = StringProperty(unique_index=True, required=True)
    topic = StringProperty(unique_index=True, required=True)
    article = Relationship("Article", "IS_SECTION_OF")
    citation = StringProperty(unique_index=True, required=True)
    clause = Relationship("Clause", "IS_SECTION_OF")
    sub_clause = Relationship("Subclause", "IS_SECTION_OF")
    case = Relationship("Case", 'IS_SECTION_OF')

```
### Clause Class

``` python

class Clause(StructuredNode):
    uuid = UniqueIdProperty()
    name = StringProperty(unique_index=True, required=True)
    topic = StringProperty(unique_index=True, required=True)
    citation = StringProperty(unique_index=True, required=True)
    article = Relationship("Article", "IS_CLAUSE_OF")
    sibling_clause= Relationship("Clause", "IS_CLAUSE_OF")
    sub_clause = Relationship("Subclause", "IS_CLAUSE_OF")
    case = Relationship("Case", 'IS_CLAUSE_OF')

```

### Subclause Class

```python

class Subclause(StructuredNode):
    uuid = UniqueIdProperty()
    name = StringProperty(unique_index=True, required=True)
    topic = StringProperty(unique_index=True, required=True)
    citation = StringProperty(unique_index=True, required=True)
    article = Relationship("Article", "'IS_SUBCLAUSE_OF'")
    clause = Relationship("Article", "'IS_SUBCLAUSE_OF'")
    sibling_clause= Relationship("Clause", "'IS_SUBCLAUSE_OF'")
    case = Relationship("Case", 'IS_SUBCLAUSE_OF')
    #sub_clause = Relationship("Subclause", "IS_SUBCLAUSE_OF")

```



## Sample Application


The application below creates a dataframe with node objects that will be uploaded to the neo4j database.  In order to accomplish an upload the .save() function must be called on the object.  


``` python

from platform import node
from pprint import pprint
#from neomodel import (config, StructuredNode, StringProperty, IntegerProperty,
#    UniqueIdProperty, RelationshipTo, BooleanProperty, EmailProperty, Relationship,db)
import pandas as pd
#import NeoNodes as nn
#import GoogleServices
#import sparkAPI as spark
import neoModelAPI as neo
import glob
import os
import json
import numpy as np
import shutil



def instantiate_neo_model_api():
    uri = "7a92f171.databases.neo4j.io"
    user = "neo4j"
    psw = 'RF4Gr2IJTNhHlW6HOrLDqz_I2E2Upyh7o8paTwfnCxg'
    return neo.neoAPI.instantiate_neo_model_session(uri=uri,user=user,psw=psw)

def get_cwd():
    cwd = os.getcwd()
    return cwd


def get_files(cwd =os.getcwd(), input_directory = 'article_data'):
    
    path = os.sep.join([cwd,input_directory])
    #pprint(path)
    file_list= [f for f in glob.glob(path + "**/*.csv", recursive=True)]
  
    return file_list

def get_df(file_list = None):
    try:
        for a_file in file_list:
            df = pd.read_csv(a_file )
            return df
    except:
        raise
       

def get_transaction_df(df = None):  
    #pprint(justice_df)
    try:
        #pprint(df.columns)
        #   df.apply(lambda x: print(x), axis =1)
        df['transaction'] = df.apply(lambda x: neo.neoAPI.create_section_node(name= x['section'],  
        topic = x['topic'], 
        citation = x['citation']),
        axis = 1
        )
        return(df)
    except:
    
        raise

def write_transaction_to_file(df, cwd = os.getcwd(),import_directory = 'merge_articles', file_name = 'article_transaction_df'):
    try:
        outfile = os.sep.join([cwd,import_directory,file_name])
        #pprint(outfile)
        df.to_csv(outfile)
        return outfile
    except:
        raise

def send_closing_message(df = None, outfile= None):
    size = shutil.get_terminal_size((80, 20))
    columns = size[0] -2


    seperator = "*" * columns
    df_message = "Your Final df looks like: "
    outfile_message = "You will find the data at: {}".format(outfile)
    pprint(seperator)
    pprint(df_message)
    pprint(df)
    pprint(seperator)
    pprint(outfile_message)
    return True
    


    


if __name__ == "__main__":
    #neo_applified = instantiate_neo_model_api()
    cwd = get_cwd()
    file_list = get_files(cwd = cwd, input_directory = 'sections_data')
    #pprint(file_list)
    #master_subject_table = create_master_subject_table()
    #json_pipeline(file_list=file_list, master_subject_table=master_subject_table)
    df = get_df(file_list = file_list)
    df = get_transaction_df(df = df)
    outfile = write_transaction_to_file(df = df , cwd = cwd, file_name = 'sections_transaction_df.csv')
    messaged = send_closing_message(df, outfile)


    #pprint(justice_df)

```

