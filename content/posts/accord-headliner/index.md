+++
title =  "Creating a GCP Client Tool"
date = "2024-04-27"
description = "GCP Submodules for repetitive tasks"
author = "Justin Napolitano"
tags = ['git', 'python', 'submodules', 'automation','workflow']
+++


# Creating a GCP Client Tool in Python

## Why

I often find myself reuuing the same bits of code when working with GCP. It is very important to avoid creating multiple development trees of the same classes. I have done this before for large projects. It will lead to a very difficult to maintain stack of tools that will spaghettify over time. 


## Creating the submodule

### Create an empty directory 

```bash
mkdir gcpuptils
```

### Add the following code to a gcpclient.py file
 
[github link to latest file](https://github.com/justin-napolitano/gcputils/blob/main/gcpclient.py) is the link to the `gcpclient.py` file on GitHub.


###  Initialize like usual 

1. Run ```git init && git add . && git commit -m 'init'```
2. run ```gh repo create``` and follow the prompts
3. run ``` git push``` and follow the prompts



## Importing into your project

In my example i created a repo at ```https://github.com/justin-napolitano/gcputils.git```

Run the following to import the latest repo into your current project. 

```bash
git submodule add -b pit https://github.com/justin-napolitano/gcputils.git

``` 

The benefit of doing this is that the code can be reused across every project without having to worry about broken development tress.  


## Using Google Cloud Storage for Python

Documentation Source: ```https://cloud.google.com/python/docs/reference/storage/latest```

### Install Google Cloud Storage for Python

Run the following 
```bash 
pip install google-cloud-storage
```

### Create the Credentials File for the Application

src = ```https://cloud.google.com/storage/docs/reference/libraries#client-libraries-install-python```

Run the following and follow the prompts

```bash
gcloud auth application-default login
```



## Initializing a client and creating a bucket to test

Source : ```https://cloud.google.com/python/docs/reference/storage/latest/google.cloud.storage.client.Client```

```python
project_id = '{YOUR PROJECT}'
gcs = GCSClient(project_id, credentials_path=None)

# List buckets to test client authorization
buckets = gcs.list_buckets()
print("Buckets:", buckets)

# creating a new bucket if it doesn't exist
bucket_name = "loc-scraper"

bucket = gcs.create_bucket(bucket_name=bucket_name)
print(bucket)
```
