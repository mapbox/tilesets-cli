import os
import sys

import click
import boto3

def upload(file, credentials):
    size = os.stat(file).st_size
    s3 = boto3.resource(
        's3',
        aws_access_key_id=credentials['accessKeyId'],
        aws_secret_access_key=credentials['secretAccessKey'],
        aws_session_token=credentials['sessionToken'],
        region_name='us-east-1'
    )

    fileobj = open(file, 'rb')
    with click.progressbar(length=size, label='{0}'.format(file), fill_char="#", empty_char='-', file=sys.stderr) as bar:
        def progress(num_bytes):
            bar.update(num_bytes)

        s3.meta.client.upload_file(file, credentials['bucket'], credentials['key'], Callback=progress)
