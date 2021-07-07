import logging

from botocore.exceptions import ClientError


def download_file_from_bucket(s3_client, bucket, folder, object_name=None):
    """Upload a file to an S3 bucket

    :param file_obj: File to upload
    :param bucket: Bucket to upload to
    :param folder: Folder to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """
    # Upload the file
    try:
        response = s3_client.download_fileobj(bucket, f"{folder}/{object_name}")
        
    except ClientError as e:
        logging.error(e)
        return False
    return response
