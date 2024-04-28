+++
title =  "GCP Cloud Run Job Scraper"
date = "2024-04-28"
description = "Running a scraper as a gcp cloud run job"
author = "Justin Napolitano"
tags = ['git', 'python', 'gcp', 'bash','workflow automation']
image = "post-image.jpeg"
featuredimage = "post-image.jpeg"
thumbnail = "post-image.jpeg"
+++


# Library of Congress Scraper Job
This [repo](https://github.com/justin-napolitano/loc_scraper) scrapes the library of congress for all of the US Supreme Court Cases available on their platform. I intent to use this data to create a research tool to better understand the corpus of text. 

## Quick History of this project
I had started work on this as an undergraduate at university, but the chatbot apis were not yet available.. and training modesl were far too expensive. I think with current tech I will be able to complete this project in about a week or two. 

### What this script does
This script simply calls the library of congress's public api with a search query and iterates through the search results.

Each result is transformed to a json string and then dropped into a gcp bucket that can be accessed by other tasks to be built into this workflow. 

## The GCP omponent
This workflow could be built for my local infrastructure or for a vm somewhere in the cloud... but I've chosen to design each task as a gcp job that will permit an enterprise scale workflow to run.
c
### Why
Because I want to push myself a bit... but this also could be used as proof of concept tool that can easily be adapted to the needs of enterprise clients or research institutions.

## Quickstart

### Download the repo

Copy the repo at [github.com/justin-napolitano/loc_scraper](https://github.com/justin-napolitano/loc_scraper) to get started

### Gcloud cli
After this you will have to install gcloud cli and configure you're local environment. I will write up some scripts in a subsequent post to automate this process... but for the time being check out this ["link"](https://cloud.google.com/sdk/docs/install)

### Create the image

In the repo there is a a bash script called ```build.sh``` that will need to be updated to according to your gcp project.

```bash
gcloud builds submit --region=us-west2 --config cloudbuild.yaml
```

It calls ```cloudbuild.yaml``` which might need to be updated for you, but the following the should work.

```yaml
steps:
- name: 'gcr.io/cloud-builders/docker'
  script: |
    docker build -t us-west2-docker.pkg.dev/$PROJECT_ID/supreme-court-scraper/supreme-court-scraper-image:dev .
  automapSubstitutions: true
images:
- 'us-west2-docker.pkg.dev/$PROJECT_ID/supreme-court-scraper/supreme-court-scraper-image:dev'
```

### Following creation of the imge 
Next you can create a job on gcp by runnning the ```job_create.sh``` script... or by copying the code below and chaging yourproject to the correct project-name

```bash
gcloud run jobs create supreme-court-scraper --image us-west2-docker.pkg.dev/yourproject/supreme-court-scraper/supreme-court-scraper-image:dev \
```

### Executing the job

Once complete you can execute the job by running the ```execute_job.sh``` script or by running 

```bash
gcloud run jobs execute supreme-court-scraper
```

### Putting it all together

In a perfect world the following should work. Note that src/.env should be set with your environmental variables such as ```$GCPPROJECTID``` 

```bash
source src/.env \
&& ./build.sh \ 
&& ./job_create.sh \
&& ./execute_job.sh
```

## Running locally

The python script in the ```/src``` can be run locally, however it should be modified if you choose not to use gcp.  There are a number of functions within that can easily be modified to permit writing to the local directory. 




