import boto3
from urllib.parse import urlparse

def read_s3_text(s3_uri: str) -> str:
    # s3_uri like s3://bucket/key...
    p = urlparse(s3_uri)
    s3 = boto3.client("s3")
    obj = s3.get_object(Bucket=p.netloc, Key=p.path.lstrip("/"))
    return obj["Body"].read().decode("utf-8", errors="ignore")
