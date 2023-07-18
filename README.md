# omniFastAPI

## Features
- Upload CSV files to Google Cloud Storage using the Google Cloud Storage API.
- Execute a query on Google BigQuery using the contents of the uploaded CSV file.
- Return the query results to the user.

## Prerequisites
- Python 3.6 or above
- Google Cloud Platform account
- Service account key file for Google Cloud Storage and Google BigQuery APIs

## Set up & Run

1. Clone the repo
`git clone https://github.com/aivan33/omniFastAPI.git`

2. Install dependencies:
`pip install -r requirements.txt`

3. Set up the Google Cloud Storage and Google BigQuery APIs:

- Create a new project on the Google Cloud Platform.
- Enable the Google Cloud Storage and Google BigQuery APIs for your project.
- Generate a service account key file and download it.
- Rename the downloaded service account key file to credentials.json and place it in the root directory of the project.

4. Configure the project:

- Open main.py and replace 'your_bucket_name' with your Google Cloud Storage bucket name.
- Update the build_query function in main.py

5. Run
`uvicorn main:app --reload`
