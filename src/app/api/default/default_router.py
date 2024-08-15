from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from app.core.logger import my_logger
from app.core.settings import my_settings

router = APIRouter(prefix="/api/v1", tags=["디폴트 API"])


@router.get("/", summary="root()", response_class=HTMLResponse)
async def root():
    """
    """
    html = f"""
        <html>
            <head>
                <title>AI Slider</title>
            </head>
            <body>
                MY_STAGE : {my_settings.my_stage} <br/>
                MY_VERSION : {my_settings.my_version} <br/>
                MY_ROOT : {my_settings.my_root} <br/>
                MY_NAME : {my_settings.my_name} <br/>
                MY_NAME : {my_settings.my_local} <br/>
                MY_TEST : {my_settings.my_test} <br/>
            </body>
        </html>
    """
    return html
