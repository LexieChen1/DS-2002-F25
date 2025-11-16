import boto3

# Create the S3 client
s3 = boto3.client("s3", region_name="us-east-1")

# CHANGE THESE:
bucket_name = "ds2002-f25-dkt4kr"       # your bucket
local_file_path = "cat.jpg"             # any local file you want to upload
s3_key = "cat.jpg"                      # destination key in S3

# Upload the file and make it PUBLIC
s3.upload_file(
    Filename=local_file_path,
    Bucket=bucket_name,
    Key=s3_key,
    ExtraArgs={"ACL": "public-read"}    # <-- makes file PUBLIC
)

print("Public upload complete!")

# Public URL formats
public_url_1 = f"https://{bucket_name}.s3.amazonaws.com/{s3_key}"
public_url_2 = f"https://{bucket_name}.s3.us-east-1.amazonaws.com/{s3_key}"

print("\nTry these URLs in your browser:")
print(public_url_1)
print(public_url_2)