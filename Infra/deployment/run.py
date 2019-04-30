import cfn
import os
import logging
from zipfile import ZipFile

stack_outputs = {}


def deploy_ddb_stack(stack):
    tmpl = open(os.path.join('../CFN', 'ddb.yaml')).read()
    ddb_params = [
        {'ParameterKey': 'DDBTableName', 'ParameterValue': 'ddb-stream'}
    ]
    stackname = 'ddb-stream'
    # stack.create_stack(stackname=stackname, template=tmpl,
    #                    parameters=ddb_params)
    stack_outputs.update(stack.stack_output(stackname))


def deploy_s3_stack(stack):
    tmpl = open(os.path.join('../CFN', 's3.yaml')).read()
    ddb_params = [
        {'ParameterKey': 'LambdaBucket', 'ParameterValue': 'jude-lambda-bucket'}
    ]
    stackname = 's3-lambda'
    # stack.create_stack(stackname=stackname, template=tmpl,
    #                    parameters=ddb_params)
    stack_outputs.update(stack.stack_output(stackname))


def upload_lamda_file(zipfile):
    # first zip lambda file
    dirctory = '../../lambda'
    file_paths = []
    for root, dirs, files in os.walk(dirctory):
        for filename in files:
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)
    print(file_paths)
    with ZipFile(zipfile, 'w') as zip:
        for file in file_paths:
            zip.write(file)


def upload_to_s3(stack, zipfile):
    client = stack.session.client('s3')
    client.upload_file(zipfile, stack_outputs['S3BucketName'], zipfile)


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
    stack.create_stack(stackname=stackname, template=tmpl,
                       parameters=lamda_params, iam='CAPABILITY_NAMED_IAM')


if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)s - %(levelname)s - %(message)s',
        level=logging.DEBUG
    )

    stack = cfn.CfnStack('default')
    deploy_ddb_stack(stack)
    deploy_s3_stack(stack)
    zipfile = 'ddb_stream_processor.zip'
    upload_lamda_file(zipfile)
    #upload_to_s3(stack, zipfile)

    #deploy_lambda_stack(stack, zipfile)
