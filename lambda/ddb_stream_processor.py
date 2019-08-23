import boto3
import botocore


def get_ddb_client():
    dynamodb = boto3.resource('dynamodb', 'us-west-2')
    table = dynamodb.Table('agg_count')
    return table


def process_image(ddb, name, image):
    key = {
        'Id': image['Id']['S'],
    }
    if name == 'INSERT':
        update_expression = 'SET alert_count = alert_count + :incre'
    elif name == 'MODIFY':
        update_expression = 'SET alert_count = alert_count - :incre'
    else:
        return

    update_obj = {
        'Key': key,
        'ConditionExpression': 'attribute_exists(alert_count)',
        'UpdateExpression': update_expression,
        'ExpressionAttributeValues': {':incre': 1}
    }
    try:
        ddb.update_item(**update_obj)
    except botocore.exceptions.ClientError as e:
        msg = str(e)
        print(msg)
        if msg.find('ConditionalCheckFailedException') > 1:
            print('adding alert_count field')
            update_obj['UpdateExpression'] = 'SET alert_count = :incre'
            update_obj['ConditionExpression'] = 'attribute_not_exists(alert_count)'
            ddb.update_item(**update_obj)
        else:
            raise


def handler(event, context):
    ddb = get_ddb_client()
    print('received event: ', event)

    try:
        print('processing event')
        for record in event['Records']:
            event_name = record['eventName']
            image = record['dynamodb']['NewImage']
            print('event', event)
            process_image(ddb, event_name, image)
    except Exception as e:
        print('unexpected error: ', str(e))
