import cfn
import os
import logging


stack_outputs = {}


def deploy_ddb_stack(stack):
    tmpl = open(os.path.join('../CFN', 'ddb.yaml')).read()
    ddb_params = [
        {'ParameterKey': 'DDBTableName', 'ParameterValue': 'ddb-stream'}
    ]
    stackname = 'ddb-stream'
    stack.create_stack(stackname=stackname, template=tmpl,
                       parameters=ddb_params)
    stack_outputs.update(stack.stack_output(stackname))


def deploy_s3_stack(stack):
    tmpl = open(os.path.join('../CFN', 's3.yaml')).read()
    ddb_params = [
        {'ParameterKey': 'LambdaBucket', 'ParameterValue': 'lambda-bucket'}
    ]
    stackname = 's3-lambda'
    stack.create_stack(stackname=stackname, template=tmpl,
                       parameters=ddb_params)
    stack_outputs.update(stack.stack_output(stackname))


def deploy_lambda_stack(stack):
    stack_outputs.update(stack.stack_output('my-network'))
    

if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)s - %(levelname)s - %(message)s',
        level=logging.DEBUG
    )

    stack = cfn.CfnStack('default')
    deploy_ddb_stack(stack)
    deploy_s3_stack(stack)
