import boto3
import json

NOTIFY_LAMBDA_NAME = "line"

lambda_client = boto3.client('lambda')

def notify_admin(message):
    payload = {
        "message": message
    }

    try:
        response = lambda_client.invoke(
            FunctionName=NOTIFY_LAMBDA_NAME,
            InvocationType='Event', 
            Payload=json.dumps(payload)
        )
        print(f"通知Lambda呼び出し成功: {response}")
    except Exception as e:
        print(f"通知Lambdaの呼び出し失敗: {str(e)}")
