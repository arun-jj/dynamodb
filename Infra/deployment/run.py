import cfn
import os
import logging
import time
from zipfile import ZipFile

stack_outputs = {}


def deploy_ddb_stack(stack):
    tmpl = open(os.path.join('../CFN', 'ddb.yaml')).read()
    ddb_params = [
        {'ParameterKey': 'DDBTableName', 'ParameterValue': 'ddb-stream'}
    ]
    stackname = 'ddb-stream'
    stack.create_or_update_stack(stackname=stackname, template=tmpl,
                                 parameters=ddb_params)
    stack_outputs.update(stack.stack_output(stackname))


def deploy_s3_stack(stack):
    tmpl = open(os.path.join('../CFN', 's3.yaml')).read()
    ddb_params = [
        {'ParameterKey': 'LambdaBucket', 'ParameterValue': 'jude-lambda-bucket'}
    ]
    stackname = 's3-lambda'
    stack.create_or_update_stack(stackname=stackname, template=tmpl,
                                 parameters=ddb_params)
    stack_outputs.update(stack.stack_output(stackname))


def zip_lamda_file(zipfile):
    cwd = os.getcwd()

    os.chdir('../../lambda')
    # first zip lambda file
    file_paths = []
    for root, dirs, files in os.walk('./'):
        for filename in files:
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)

    with ZipFile(zipfile, 'w') as zip:
        for file in file_paths:
            zip.write(file)

    os.chdir(cwd)

def upload_to_s3(stack, filename, key):
    client = stack.session.client('s3')
    client.upload_file(zipfile, stack_outputs['S3BucketName'], key)
    time.sleep(10)

def update_lambda_function(stack, key):
    lm_client = stack.session.client('lambda')
    lm_client.update_function_code(
        FunctionName='ddb_stream_processor',
        S3Bucket=stack_outputs['S3BucketName'],
        S3Key=key
    )

def deploy_lambda_stack(stack, zipfile):
    stack_outputs.update(stack.stack_output('my-network'))
    tmpl = open(os.path.join('../CFN', 'lambda.yaml')).read()
    lamda_params = [
        {'ParameterKey': 'CodeS3Bucket', 'ParameterValue': stack_outputs['S3BucketName']},
        {'ParameterKey': 'CodeS3Key', 'ParameterValue': zipfile},
        {'ParameterKey': 'ResourceSecurityGroup', 'ParameterValue': 'sg-0c2be3c91661c5eaf'},
        {'ParameterKey':  'ResourceSubnet', 'ParameterValue': stack_outputs['Subnet1Id']},
        {'ParameterKey': 'DDBTableName', 'ParameterValue': stack_outputs['DDBTableName']}
    ]
    stackname = 'ddb-stream-lambda'
    stack.create_or_update_stack(stackname=stackname, template=tmpl,
                                 parameters=lamda_params, iam='CAPABILITY_NAMED_IAM')


if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)s - %(levelname)s - %(message)s',
        level=logging.DEBUG
    )

    stack = cfn.CfnStack('default')
    deploy_ddb_stack(stack)
    deploy_s3_stack(stack)
    key = 'ddb_stream_processor.zip'
    zip_lamda_file(key)

    zipfile = '../../lambda/' + key
    upload_to_s3(stack, zipfile, key)
    deploy_lambda_stack(stack, key)
    update_lambda_function(stack, key)
