# Deploying to Cloud Run (one-time setup)

Flow: push to `main` -> GitHub Actions runs tests -> builds image -> pushes to Artifact Registry -> deploys to Cloud Run. The API writes the CSV to a GCS bucket.

Replace the values in CAPS. Run in a terminal after `gcloud auth login`.

```bash
export PROJECT_ID=YOUR_PROJECT_ID
export REGION=asia-south1
export BUCKET=${PROJECT_ID}-weather-csv
export GH_REPO=YOUR_GITHUB_USER/YOUR_REPO
gcloud config set project $PROJECT_ID

# 1. APIs
gcloud services enable run.googleapis.com artifactregistry.googleapis.com \
  iamcredentials.googleapis.com storage.googleapis.com

# 2. Bucket and image repository
gcloud storage buckets create gs://$BUCKET --location=$REGION
gcloud artifacts repositories create weather --repository-format=docker --location=$REGION

# 3. Runtime service account (the identity the API runs as)
gcloud iam service-accounts create weather-runtime
gcloud storage buckets add-iam-policy-binding gs://$BUCKET \
  --member="serviceAccount:weather-runtime@$PROJECT_ID.iam.gserviceaccount.com" \
  --role=roles/storage.objectUser

# 4. Deployer service account (the identity GitHub Actions uses)
gcloud iam service-accounts create github-deployer
for ROLE in roles/run.admin roles/artifactregistry.writer; do
  gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:github-deployer@$PROJECT_ID.iam.gserviceaccount.com" --role=$ROLE
done
# lets the deployer start Cloud Run services that run as weather-runtime
gcloud iam service-accounts add-iam-policy-binding \
  weather-runtime@$PROJECT_ID.iam.gserviceaccount.com \
  --member="serviceAccount:github-deployer@$PROJECT_ID.iam.gserviceaccount.com" \
  --role=roles/iam.serviceAccountUser

# 5. Workload Identity Federation (GitHub logs in without a key file)
gcloud iam workload-identity-pools create github --location=global
gcloud iam workload-identity-pools providers create-oidc github-provider \
  --location=global --workload-identity-pool=github \
  --issuer-uri="https://token.actions.githubusercontent.com" \
  --attribute-mapping="google.subject=assertion.sub,attribute.repository=assertion.repository" \
  --attribute-condition="assertion.repository=='$GH_REPO'"
PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID --format='value(projectNumber)')
gcloud iam service-accounts add-iam-policy-binding \
  github-deployer@$PROJECT_ID.iam.gserviceaccount.com \
  --role=roles/iam.workloadIdentityUser \
  --member="principalSet://iam.googleapis.com/projects/$PROJECT_NUMBER/locations/global/workloadIdentityPools/github/attribute.repository/$GH_REPO"
echo "WIF_PROVIDER=projects/$PROJECT_NUMBER/locations/global/workloadIdentityPools/github/providers/github-provider"
```

## GitHub repository variables

Settings -> Secrets and variables -> Actions -> **Variables**:

| Name | Value |
|---|---|
| `GCP_PROJECT_ID` | your project ID |
| `GCP_REGION` | `asia-south1` |
| `GCS_BUCKET` | the bucket name from step 2 |
| `WIF_PROVIDER` | the value printed by the last command |
| `DEPLOYER_SA` | `github-deployer@PROJECT_ID.iam.gserviceaccount.com` |
| `RUNTIME_SA` | `weather-runtime@PROJECT_ID.iam.gserviceaccount.com` |

None of these is a secret, and no key file is needed.

## Calling the deployed API

The service is private (`--no-allow-unauthenticated`). Call it with your own identity token:

```bash
URL=$(gcloud run services describe weather-etl-api --region $REGION --format='value(status.url)')
curl -X POST -H "Authorization: Bearer $(gcloud auth print-identity-token)" $URL/run
curl -H "Authorization: Bearer $(gcloud auth print-identity-token)" -o forecast.csv $URL/forecast.csv
```

Your account needs the **Cloud Run Invoker** role on the service.
