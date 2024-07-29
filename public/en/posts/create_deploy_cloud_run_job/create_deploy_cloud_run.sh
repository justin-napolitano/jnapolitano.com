#!/bin/bash

# Check if the correct number of arguments are provided
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 PROJECT_NAME IMAGE_NAME JOB_NAME"
    exit 1
fi

# Assign arguments to variables
PROJECT_NAME=$1
IMAGE_NAME=$2
JOB_NAME=$3
REGION="us-west2"
SERVICE_ACCOUNT="general-purpose-account@${PROJECT_NAME}.iam.gserviceaccount.com"
DOCKERFILE_PATH="Dockerfile"

# Create cloudbuild.yaml
cat <<EOF > cloudbuild.yaml
steps:
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'gcr.io/$PROJECT_NAME/$IMAGE_NAME', '.']

  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'gcr.io/$PROJECT_NAME/$IMAGE_NAME']

  - name: 'gcr.io/cloud-builders/gcloud'
    args: ['run', 'jobs', 'create', '$JOB_NAME',
           '--image', 'gcr.io/$PROJECT_NAME/$IMAGE_NAME',
           '--region', '$REGION']
    # UNcomment if necessary.s
    # env:
    #   - 'CLOUDSDK_AUTH_CREDENTIAL_FILE_OVERRIDE=/workspace/keys/service-account-key.json'

timeout: '1200s'
EOF

# Ensure the service account key JSON file exists
#Depending on the use case uncomment this
# if [ ! -f "keys/service-account-key.json" ]; then
#     echo "Service account key file (keys/service-account-key.json) not found!"
#     exit 1
# fi

# Submit the build to Google Cloud Build
gcloud builds submit --config cloudbuild.yaml .

# Run the job
gcloud run jobs execute $JOB_NAME --region $REGION

echo "Cloud Run job '$JOB_NAME' created and executed successfully."
