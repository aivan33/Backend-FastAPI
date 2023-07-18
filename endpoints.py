@app.post("/upload-csv")
async def upload_csv(file: UploadFile = File(...)):
    """Uploads a CSV file to Google Cloud Storage"""
    if file.filename.endswith('.csv'):
        save_file_to_gcs(file, file.filename)
        return {"message": "File uploaded successfully!"}
    else:
        raise HTTPException(status_code=400, detail="Uploaded file is not a CSV file")

@app.post("/query/{table_name}")
async def query(table_name: str, filename: str):
    """Executes a query on BigQuery using the specified CSV file"""
    csv_data = read_file_from_gcs(filename)
    result = read_csv_and_run_query(csv_data, table_name)
    return {"result": result}
