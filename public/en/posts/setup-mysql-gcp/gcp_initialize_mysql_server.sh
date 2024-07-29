#!/bin/bash

# Source the .env file to load environment variables
set -o allexport
source .env
set -o allexport

# Set other variables
PROJECT_ID="smart-axis-421517"
INSTANCE_NAME="jnapolitano-site"
REGION="us-west2" # e.g., us-central1
DATABASE_NAME="jnapolitano"
BUILDS_SQL_FILE="/home/cobra/Repos/justin-napolitano/setup-mysql-gcp/mysql-config/builds.sql" # Name of your builds SQL file
FEED_SQL_FILE="/home/cobra/Repos/justin-napolitano/setup-mysql-gcp/mysql-config/feed.sql"   # Name of your feeds SQL file

# Authenticate with GCP (make sure you have gcloud SDK installed and authenticated)
gcloud auth login

# Set the project
gcloud config set project $PROJECT_ID


# Enable the Cloud SQL Admin API
gcloud services enable sqladmin.googleapis.com


# Create a Cloud SQL instance
gcloud sql instances create $INSTANCE_NAME \
    --database-version=MYSQL_8_0 \
    --cpu=2 \
    --memory=7680MB \
    --region=$REGION

# Set the root password using environment variable
gcloud sql users set-password root \
    --host=% \
    --instance=$INSTANCE_NAME \
    --password=$ROOT_PASSWORD

# Create a user called 'cobra' using environment variable
gcloud sql users create cobra \
    --host=% \
    --instance=$INSTANCE_NAME \
    --password=$COBRA_PASSWORD

# Grant superuser privileges to 'cobra' and ensure host is '%'
gcloud sql connect $INSTANCE_NAME --user=root --quiet << EOF
CREATE USER IF NOT EXISTS 'cobra'@'%' IDENTIFIED BY '$COBRA_PASSWORD';
GRANT ALL PRIVILEGES ON *.* TO 'cobra'@'%' WITH GRANT OPTION;
FLUSH PRIVILEGES;
EOF

# Optional: Create a database (uncomment if needed)
# DATABASE_NAME="your-database-name"
# gcloud sql databases create $DATABASE_NAME --instance=$INSTANCE_NAME

# Create a database
gcloud sql databases create $DATABASE_NAME --instance=$INSTANCE_NAME

# Execute the SQL files to create the 'builds' and 'feeds' tables
gcloud sql connect $INSTANCE_NAME --user=cobra  < $BUILDS_SQL_FILE
gcloud sql connect $INSTANCE_NAME --user=cobra  < $FEED_SQL_FILE


echo "MySQL instance $INSTANCE_NAME created successfully in project $PROJECT_ID with superuser 'cobra' and executed SQL files '$BUILDS_SQL_FILE' and '$FEEDS_SQL_FILE'."
