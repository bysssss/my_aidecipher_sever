import json
import os
import platform
import sys

from app.core.logger import my_logger
from app.core.settings import my_settings
from app.worker import switch
from app.util import file_util


def lambda_handler(event, context):
    pretty = json.dumps({
        "event": event,
        "context": str(context),
        "platform": platform.uname(),
        "python": sys.version,
        "cwd": os.getcwd(),
        "AWS_PROFILE": os.getenv('AWS_PROFILE'),
        "AWS_CONFIG_FILE": os.getenv('AWS_CONFIG_FILE'),
        "AWS_SHARED_CREDENTIALS_FILE": os.getenv('AWS_SHARED_CREDENTIALS_FILE'),
        "AWS_DEFAULT_REGION": os.getenv('AWS_DEFAULT_REGION'),
    })
    my_logger.info(f"worker() : {pretty}")

    return switch.adapt(event)


if __name__ == "__main__":
    test = file_util.read_json(f"/src/resource/lambda/test.json")
    lambda_handler(test, None)
