import json
from functools import lru_cache

from fastapi import Depends, HTTPException, status

from app.core.logger import my_logger
from app.config.aws_config import init_lambda_client


class AwsLambda:
    def __init__(self, lambda_client):
        self.lambda_client = lambda_client
        print(f"init AwsLambda")

    def __hash__(self):
        return hash(self.lambda_client)

    def invoke(self, function_name, invocation_type, payload):
        try:
            # RequestResponse=synchronously, Event=asynchronously, DryRun=단순히 검사용?
            func = self.lambda_client.invoke(FunctionName=function_name, InvocationType=invocation_type, Payload=json.dumps(payload))
            my_logger.info(f"aws_lambda.invoke() : func={func}")
        except Exception as e:
            my_logger.error(f"aws_lambda.invoke() : e={e}")
            raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(e), headers={'X': 'aws_lambda'})
        return func


@lru_cache()
def inject_aws_lambda(
        lambda_client=Depends(init_lambda_client)
):
    print(f"inject_aws_lambda()")
    return AwsLambda(lambda_client=lambda_client)
