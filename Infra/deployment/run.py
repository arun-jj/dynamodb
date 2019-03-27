import cfn
import os
import logging


if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)s - %(levelname)s - %(message)s',
        level=logging.DEBUG
    )

    stack = cfn.CfnStack('default')
    tmpl = open(os.path.join('../CFN', 'ddb.yaml')).read()
    ddb_params = [
        {'ParameterKey': 'DDBTableName', 'ParameterValue': 'ddb-stream'}
    ]

    stack.create_stack(stackname='ddb-stream', template=tmpl,
                       parameters=ddb_params)
