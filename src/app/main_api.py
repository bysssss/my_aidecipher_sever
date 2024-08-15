import json
import os
import platform
import sys

from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from mangum import Mangum

from app import init_router, init_cors, init_handler, init_middleware
from app.core.logger import my_logger
from app.core.settings import my_settings


def create_app() -> FastAPI:
    template = Jinja2Templates(directory='resource/jinja').get_template('openapi-desc.html')
    my_app = FastAPI(
        title='AI Slider',
        description=template.render(),
        version=f"{my_settings.my_version}",
        root_path=f"{my_settings.my_root}",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    init_router(my_app)
    init_cors(my_app)
    init_middleware(my_app)
    init_handler(my_app)

    return my_app


my_fastapi = create_app()


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
    my_logger.info(f"api() : {pretty}")

    asgi_adapter = Mangum(my_fastapi, lifespan="auto")
    return asgi_adapter(event, context)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main_api:my_fastapi",
        reload=False,
        host="0.0.0.0",
        port=5000,
        log_level="info",
    )
