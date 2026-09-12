import json
import boto3
import urllib.parse

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')

def handler(event, context):
    record = event['Records'][0]
    bucket = record['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(record['s3']['object']['key'])

    response = s3.head_object(Bucket=bucket, Key=key)
    size = response['ContentLength']
    content_type = response.get('ContentType', 'unknown')

    table = dynamodb.Table('serverless-pipeline-files')
    table.put_item(Item={
        'file_key': key,
        'bucket': bucket,
        'size_bytes': size,
        'content_type': content_type
    })

    print(f"Processed {key}: {size} bytes, type {content_type}")
    return {"statusCode": 200}