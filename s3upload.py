import boto3
from botocore.exceptions import NoCredentialsError

# Create an S3 client
s3 = boto3.client('s3')

def upload_pdf_to_s3(file_path, bucket_name, s3_key):
    try:
        # Upload the PDF file to S3
        s3.upload_file(file_path, bucket_name, s3_key)
        print(f"File {file_path} uploaded to {bucket_name}/{s3_key}")
    except FileNotFoundError:
        print(f"File {file_path} not found.")
    except NoCredentialsError:
        print("Credentials not available.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Specify the local PDF file, bucket name, and the S3 destination path
local_pdf_path = 'path/to/your/generated_pdf.pdf'
bucket_name = 'abc'
s3_key = 'def/ghi/generated_pdf.pdf'

# Upload the file
upload_pdf_to_s3(local_pdf_path, bucket_name, s3_key)
