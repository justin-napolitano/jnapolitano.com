output=$(gcloud config get-value project)
export PROJECTID=$output
# Setting up the config for docker 
gcloud auth configure-docker us-central1-docker.pkg.dev,us-east1-docker.pkg.dev, us-west2-docker.pkg.dev

