gcloud artifacts repositories create $APPNAME --repository-format=docker \
    --location=$GCPREGION --description="'$PROJECTDESCRIPTION'"
