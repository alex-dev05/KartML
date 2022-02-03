from google.cloud import bigquery
import os
import glob
import csv

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "c:\Poli\Dizertatie\cloud-computing-305617-91437ff4f742.json"
    
client = bigquery.Client()

table_id = "cloud-computing-305617.Kart_Agent_Data.Records"

list_of_files = glob.glob('C:\Poli\Dizertatie\Repo_Github\KartML\Export_Csv\*.csv') # * means all if need specific format then *.csv
latest_file = max(list_of_files, key=os.path.getctime)
print(latest_file)

job_config = bigquery.LoadJobConfig(
    source_format=bigquery.SourceFormat.CSV, skip_leading_rows=1, autodetect=True,
)

with open(latest_file, "rb") as source_file:
    job = client.load_table_from_file(source_file, table_id, job_config=job_config)

job.result()  # Waits for the job to complete.

table = client.get_table(table_id)  # Make an API request.
print(
    "Loaded {} rows and {} columns to {}".format(
        table.num_rows, len(table.schema), table_id
    )
)
