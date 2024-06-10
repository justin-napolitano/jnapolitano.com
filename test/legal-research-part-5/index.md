+++
title = "Conduct Legal Research with AI: Part 5"
date = "2022-05-21T14:30:32.169Z"
description = "Transforming the Library of Congress results into individual json documents contaning case information."
author = "Justin Napolitano"
image = "post-image.jpeg"
categories = ['Legal Research', 'Data Wrangling', 'Graph Database', 'Automation']
tags = ['python','legal', 'json', 'scotus', 'automation']
images = ['feature-image.png']
series = ['Legal Research with AI']
+++

# Legal Research with AI: Part 5"

In the previous posts in this series, I have downloaded the data required to build the neo4j graph.  In this post, I will arrange the data into a data structure that will permit me to easily create graph nodes and most importantly relationships.  

## The Runner Program

The raw structure of the data is organized by the results of the api requests.  There are thus 80 cases per file.  I want them organized by individual cases to facilitate integration with another dataset that will be detailed in the next post.  

### Glob the input older
The program below simply reads thedownloaded json data from a folder to create a list of file paths to read. 

### Modify The Case Data

It then traverses that list to find the individual case data to write to file.  

### Add  `loc_id` to the Dictionary

For each case it create the `loc_id` key that will be used to join with another dataset. 

### Write to File

Finally, it writes the new case dictionary to file.  



```Python

import pandas as pd
import glob
import os
import json
import numpy as np
from pprint import pprint
import re
#from neoModelAPI import NeoNodes as nn




    

def get_cwd():
    cwd = os.getcwd()
    return cwd

def get_files(cwd =os.getcwd(), input_directory = 'loc_cases'):
    
    path = os.sep.join([cwd,input_directory])
    file_list= [f for f in glob.glob(path + "**/*.json", recursive=True)]
  
    return file_list



def load_json_data(file):
    f = open (file, "r")
  
    # Reading from file
    data = json.loads(f.read())
    return data

def citation_output(file_list,cwd):
    outpath = os.sep.join([cwd,'loc_cited'])
    for file in file_list:
        
        data = load_json_data(file=file)
        data = data['results']
        #data = create_citation(data)
        for result in data:
            split = result['id'].split('/')
            result['loc_id'] = split[4]
            outfile = split[4] + '.json'
            outfile = os.sep.join([outpath,outfile])
            
            pprint(outfile)
            with open(outfile, 'w') as f:
                json.dump(result, f)



if __name__ == "__main__":
    #neo_applified = instantiate_neo_model_api()
    cwd = get_cwd()
    file_list = get_files(cwd = cwd)
    output_files = citation_output(file_list,cwd)

```
