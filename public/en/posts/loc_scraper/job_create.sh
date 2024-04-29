# gcloud run jobs deploy job-quickstart \
#     --source . \
#     --tasks 50 \
#     --set-env-vars SLEEP_MS=10000 \
#     --set-env-vars FAIL_RATE=0.1 \
#     --max-retries 5 \
#     --region REGION \
#     --project=PROJECT_ID


gcloud run jobs create supreme-court-scraper --image us-west2-docker.pkg.dev/$GCPPROJECTID/supreme-court-scraper/supreme-court-scraper-image:dev \
    --max-retries 5 \
    --region us-west2 \
    --project=smart-axis-421517
