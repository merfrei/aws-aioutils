"""
AWS S3 - Utils
"""

import logging
import aioboto3
from botocore.exceptions import ClientError


class Bucket:
    '''Utils to manage objects/files in a bucket S3'''

    def __init__(self, bucket_name: str, endpoint_url: str = None):
        self.bucket = bucket_name
        self.endpoint_url = endpoint_url

    async def file_exists(self, object_name: str):
        '''Check if an object exists in the bucket'''
        session = aioboto3.Session()
        async with session.resource('s3', endpoint_url=self.endpoint_url) as s3_res:
            try:
                s3_obj = await s3_res.Object(self.bucket, object_name)
                await s3_obj.load()
            except ClientError as exp:
                if exp.response['Error']['Code'] == '404':
                    return False
                # Something else has gone wrong.
                raise
            return True

    async def delete_file(self, object_name: str):
        '''Delete/remove an object from the bucket'''
        session = aioboto3.Session()
        async with session.resource('s3', endpoint_url=self.endpoint_url) as s3_res:
            s3_object = await s3_res.Object(self.bucket, object_name)
            await s3_object.delete()

    async def download_file(self, object_name: str, file_name: str):
        '''Download an object from an S3 bucket and write it to a local file
        :param object_name: S3 object name
        :param file_name: File where the object will be stored
        '''
        session = aioboto3.Session()
        async with session.client('s3', endpoint_url=self.endpoint_url) as s3_cli:
            with open(file_name, 'wb') as f_obj:
                await s3_cli.download_fileobj(self.bucket, object_name, f_obj)

    async def upload_file(self, file_name: str, object_name: str = None):
        '''Upload a file to an S3 bucket
        :param file_name: File to upload
        :param object_name: S3 object name. If not specified then file_name is used
        :return: True if file was uploaded, else False
        '''

        # If S3 object_name was not specified, use file_name
        if object_name is None:
            object_name = file_name

        # Upload the file

        session = aioboto3.Session()
        async with session.client('s3', endpoint_url=self.endpoint_url) as s3_cli:
            try:
                _ = await s3_cli.upload_file(file_name, self.bucket, object_name)
            except ClientError as exp:
                logging.error(exp)
                return False
            return True

    async def create_presigned_url(self, object_name: str, expiration: int = 3600):
        '''Generate a presigned URL to share an S3 object
        :param object_name: string
        :param expiration: Time in seconds for the presigned URL to remain valid
        :return: Presigned URL as string. If error, returns None.
        '''

        # Generate a presigned URL for the S3 object
        session = aioboto3.Session()
        async with session.client('s3', endpoint_url=self.endpoint_url) as s3_cli:
            try:
                response = await s3_cli.generate_presigned_url('get_object',
                                                               Params={'Bucket': self.bucket,
                                                                       'Key': object_name},
                                                               ExpiresIn=expiration)
            except ClientError as exp:
                logging.error(exp)
                return None

            # The response contains the presigned URL
            return response
