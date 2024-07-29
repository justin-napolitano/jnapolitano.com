#!/bin/bash

# Variables
PROJECT_ID="your-google-cloud-project-id"
IMAGE_NAME="your-image-name"
SERVICE_NAME="your-cloud-run-service-name"
REGION="your-region"  # e.g., us-central1

# Authenticate with Google Cloud
gcloud auth login

# Set the project
gcloud config set project $PROJECT_ID

# Enable necessary services
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com

# Build the Docker image
docker build -t gcr.io/$PROJECT_ID/$IMAGE_NAME .

# Push the Docker image to Google Container Registry
docker push gcr.io/$PROJECT_ID/$IMAGE_NAME

# Deploy to Cloud Run
gcloud run deploy $SERVICE_NAME \
  --image gcr.io/$PROJECT_ID/$IMAGE_NAME \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated
