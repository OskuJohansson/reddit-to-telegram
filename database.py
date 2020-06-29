import boto3
from os import environ
from botocore.exceptions import ClientError


def __get_dynamodb():
    region = environ["aws_dynamodb_region"]
    dynamodb = boto3.resource('dynamodb', region)
    # Use this for local testing. Requires dynamodb-local Docker container running
    # dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000')
    return dynamodb


def get_buffer():
    dynamodb = __get_dynamodb()
    table_name = environ["aws_dynamodb_buffer_table_name"]
    table = dynamodb.Table(table_name)

    response = table.get_item(
        Key={
            'id': 1
        }
    )

    if "Item" in response:
        item = response["Item"]
        buffer = item["buffer"]
        return buffer
    else:
        print("Buffer doesn't exist, danger danger!")
        return []


def put_in_buffer(new_posts):
    dynamodb = __get_dynamodb()
    table_name = environ["aws_dynamodb_buffer_table_name"]
    table = dynamodb.Table(table_name)

    table.update_item(
        Key={
            'id': 1
        },
        UpdateExpression="SET #b = list_append(#b, :vals)",
        ExpressionAttributeNames={
            '#b': 'buffer'
        },
        ExpressionAttributeValues={
            ':vals': new_posts
        },
        ReturnValues="UPDATED_NEW"
    )


def update_buffer(updated_buffer):
    dynamodb = __get_dynamodb()
    table_name = environ["aws_dynamodb_buffer_table_name"]
    table = dynamodb.Table(table_name)

    table.update_item(
        Key={
            'id': 1
        },
        UpdateExpression="SET #b = :vals",
        ExpressionAttributeNames={
            '#b': 'buffer'
        },
        ExpressionAttributeValues={
            ':vals': updated_buffer
        },
        ReturnValues="UPDATED_NEW"
    )


def put_to_archive(post):
    dynamodb = __get_dynamodb()
    table_name = environ["aws_dynamodb_archive_table_name"]
    table = dynamodb.Table(table_name)
    table.put_item(
        Item={
            'id': post.id,
            'date': int(post.created_utc)
        }
    )
