import boto3
import uuid
from datetime import datetime


session = boto3.session.Session(profile_name='default')
dynamodb = session.resource('dynamodb', 'us-west-2')
table = dynamodb.Table('ddb-stream')


acc1 = 'ACC-1'
acc2 = 'ACC-2'

item = {
    'Id': acc2,
    'timestamp_count': int(datetime.utcnow().timestamp() * 1000000),
    'status': 1
}
table.put_item(Item=item)


# update_obj = {
#     'Key': {'Id': acc1, 'timestamp_count': 1557360471509589},
#     'UpdateExpression': 'SET #status=:status_val',
#     'ExpressionAttributeNames': {'#status': 'status'},
#     'ExpressionAttributeValues': {':status_val': 0}
# }
# table.update_item(**update_obj)


# def get_ddb_client():
#     dynamodb = boto3.resource('dynamodb', 'us-west-2')
#     table = dynamodb.Table('ddb-stream')
#     return table
#
#
# def handle_event(ddb, event, image):
#     key = {
#         'Id': image['Id']['S'],
#         'timestamp_count': 0
#     }
#     if event == 'INSERT':
#         update_expression = 'SET alert_count = alert_count + :incre'
#     elif event == 'MODIFY':
#         update_expression = 'SET alert_count = alert_count - :incre'
#
#     update_obj = {
#         'Key': key,
#         'ConditionExpression': 'attribute_exists(alert_count)',
#         'UpdateExpression': update_expression,
#         'ExpressionAttributeValues': {':incre': 1}
#     }
#     try:
#         ddb.update_item(**update_obj)
#     except Exception as e:
#         msg = str(e)
#         if msg.find('ConditionalCheckFailedException') > 1:
#             update_obj['UpdateExpression'] = 'SET alert_count = :incre'
#             update_obj['ConditionExpression'] = 'attribute_not_exists(alert_count)'
#             ddb.update_item(**update_obj)
#         else:
#             raise
#
#
# def handler():
#     # ddb = get_ddb_client()
#     event = {
#         'Records': [
#             {
#                 'eventID': '41ea110b46ea5b3b546155f5681dfdaf',
#                 'eventName': 'INSERT',
#                 'eventVersion': '1.1',
#                 'eventSource': 'aws:dynamodb',
#                 'awsRegion': 'us-west-2',
#                 'dynamodb': {
#                     'ApproximateCreationDateTime': 1557329697.0,
#                     'Keys': {
#                         'timestamp_count': {'N': '1557344097039248'},
#                         'Id': {'S': 'ACC-1'}
#                     },
#                     'NewImage': {
#                         'timestamp_count': {'N': '1557344097039248'},
#                         'Id': {'S': 'ACC-1'},
#                         'status': {'N': '1'}
#                     },
#                     'SequenceNumber': '40215500000000001429493809',
#                     'SizeBytes': 70, 'StreamViewType': 'NEW_IMAGE'
#                 },
#                 'eventSourceARN': 'arn:aws:dynamodb:us-west-2:177286222258:table/ddb-stream/stream/2019-04-30T03:04:37.097'
#             }
#         ]
#     }
#     for record in event['Records']:
#         event = record['eventName']
#         image = record['dynamodb']['NewImage']
#         handle_event(table, event, image)
#
#
# handler()
