import boto3
import uuid
from datetime import datetime


session = boto3.session.Session(profile_name='default')
dynamodb = session.resource('dynamodb', 'us-west-2')
table = dynamodb.Table('ddb-stream')


item = {
    'Id': str(uuid.uuid4()),
    'timestamp_count': int(datetime.utcnow().timestamp() * 1000000),
    'status': 1
}
# table.put_item(Item=item)


update_obj = {
    'Key': {'Id': 'ce96a4a9-4725-4ec5-bdb6-d64e12ea173a', 'timestamp_count': 1557125993172217},
    'UpdateExpression': 'SET #status=:status_val',
    'ExpressionAttributeNames': {'#status': 'status'},
    'ExpressionAttributeValues': {':status_val': 0}
}
table.update_item(**update_obj)
