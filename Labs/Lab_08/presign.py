import boto3
import requests
import argparse

def download_file(url, local_path):
    print(f"Downloading file from {url} ...")
    r = requests.get(url)
    r.raise_for_status()        
    with open(local_path, "wb") as f:
        f.write(r.content)
    print(f"Saved file to {local_path}")

def upload_to_s3(local_path, bucket, key):
    print(f"Uploading {local_path} to s3://{bucket}/{key} ...")
    s3 = boto3.client('s3', region_name="us-east-1")
    s3.upload_file(local_path, bucket, key)
    print("Upload complete!")

def presign_url(bucket, key, expires):
    print("Generating presigned URL...")
    s3 = boto3.client('s3', region_name="us-east-1")
    url = s3.generate_presigned_url(
        'get_object',
        Params={'Bucket': bucket, 'Key': key},
        ExpiresIn=expires
    )
    return url

def main():
    parser = argparse.ArgumentParser(description="Download, upload to S3, and presign a file.")
    parser.add_argument("url", help="URL of file to download")
    parser.add_argument("bucket", help="S3 bucket name")
    parser.add_argument("key", help="S3 key (destination filename in bucket)")
    parser.add_argument("expires", type=int, help="Presigned URL expiration in seconds")

    args = parser.parse_args()

    # Step 1: Download file
    local_filename = args.key  # save local file with same name as S3 key
    download_file(args.url, local_filename)

    # Step 2: Upload to S3
    upload_to_s3(local_filename, args.bucket, args.key)

    # Step 3: Presign
    url = presign_url(args.bucket, args.key, args.expires)

    # Step 4: Output
    print("\nPresigned URL:")
    print(url)

if __name__ == "__main__":
    main()