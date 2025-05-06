import os
import boto3
from botocore.exceptions import ClientError

# DynamoDBテーブル名
TABLE_NAME =os.getenv('DYNAMO_TABLE_NAME') 

# DynamoDBリソースの初期化
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(TABLE_NAME)

def get_current_title_and_url():
    """
    DynamoDBから現在のタイトルとURLを取得する。
    :returns: 現在のタイトルとURLが格納された辞書、またはNone
    """
    try:
        response = table.get_item(Key={'data_id': 'penelope'})
        # 'Item'は存在しない場合Noneを返す
        return response.get('Item', None)
    except ClientError as e:
        print(f"Error fetching data from DynamoDB: {e}")
        raise e

def update_title_and_url(new_title, new_url):
    """
    DynamoDBのタイトルとURLを更新する。
    :param new_title: 新しいタイトル
    :param new_url: 新しいURL
    """
    try:
        response = table.update_item(
            Key={'data_id': 'penelope'},
            UpdateExpression="SET title = :title, page_url = :page_url",
            ExpressionAttributeValues={
                ':title': new_title,
                ':page_url': new_url
            },
            ReturnValues="UPDATED_NEW"  # 更新内容を返す
        )
        print(f"Successfully updated title and URL in DynamoDB: {response}")
        return response
    except ClientError as e:
        print(f"Error updating data in DynamoDB: {e}")
        raise e