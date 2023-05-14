# API - AIzaSyDQTfAOLcUNuKOOSS7gI1aZ9ylfwGivupw
from fastapi import FastAPI, UploadFile, HTTPException, Form
from google.cloud import storage, bigquery
from typing import Annotated

app = FastAPI()
client = bigquery.Client()


# class CSV(BaseModel):
# Service account key for Google Cloud authentication
#    gcloud_service_account_key: Annotated[str, Form()]

#    csv_id: str  # ID associated with the uploaded CSV file


@app.post("/uploadfile/")
def csv_upload(
    gcloud_service_api_key: Annotated[str, Form()],
    csv_id: Annotated[str, Form()],
    csv: UploadFile,
):

    csv_content = csv.file.read()  # Read the content of the uploaded CSV file

    if not csv.filename.endswith('.csv'):
        raise HTTPException(
            status_code=400, detail="The uploaded file is not a CSV")

# Initialize the Google Cloud Storage client with the provided service account key
    storage_client = storage.Client(client_options={
        "quota_project_id": "omniproject-51",
        "api_key": gcloud_service_api_key,
    })
    bucket_name = storage_client.bucket("api_tester")  # Specify target bucket
    # Create a blob for the uploaded file
    blob = bucket_name.blob(csv_upload.csv_id)

    blob.upload_from_string(csv_content)  # Upload the file to the bucket

    # Construct BigQuery table
    table_name = csv.filename[:-4]  # Use CSV filename as the table name
    dataset_id = "api_tester"  # Specify target dataset

    job_config = bigquery.LoadJobConfig(
        autodetect=True,  # Detect the schema based on the CSV file
        # skip_leading_rows = 1,
        source_format=bigquery.SourceFormat.CSV

    )
    # Used Bobi's code as ref
    uri = f"gs://api_tester/{csv_id}"
    load_job = client.load_table_from_uri(
        uri, table_name, job_config=job_config)

    try:
        load_job.result()
    except:
        raise HTTPException(
            status_code=400, detail="CSV file has incosistencies or is not a CSV"
        )
    client.get_table(table_name)
    return "Upload was successful"


@app.post("/query/")
def query(
    gcloud_service_api_key: Annotated[str, Form()],
    csv_id: Annotated[str, Form()],
    query: Annotated[str, Form()]
):
    client = bigquery.Client(
        client_options={
            "quota_project_id": "omniproject-51",
            "api_key": gcloud_service_api_key,
        }
    )
    run_query = client.query(query)
    try:
        run_query.result()
    except:
        raise HTTPException(
            status_code=400, detail="Query failed to execute"
        )
    rows = run_query.result()
    # rows = list(data)
    return rows
