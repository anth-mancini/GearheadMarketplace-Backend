import logging

from botocore.exceptions import ClientError


def delete_file_from_bucket(s3_client, file_obj, bucket, folder):
    response = s3_client.delete_object(Bucket=bucket, Key=f"{folder}/{file_obj}")
    return response

