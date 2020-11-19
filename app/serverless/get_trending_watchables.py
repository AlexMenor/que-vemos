import json

def get_trending_watchables(event, context):
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }