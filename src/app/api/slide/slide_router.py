from typing import Optional

from fastapi import APIRouter, Depends, Security, Header, Path, Query, Body, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from app.core.logger import my_logger
from app.config.auth_config import MyAuth, init_auth
from app.common.common_spec import ErrRes
from app.api.slide.slide_api import SlideApi, inject_slide_api
from app.api.slide.slide_spec import SlidePostReq, SlideRes, SlidesRes
from app.type.scope_type import ScopeType

router = APIRouter(prefix="/api/v1/slide", tags=["슬라이드 API"])


@router.get("/{slide_id}", summary="슬라이드 조회 (for download)", responses={
    200: {"model": SlideRes},
    401: {"model": ErrRes},
    403: {"model": ErrRes},
    422: {"model": ErrRes},
    500: {"model": ErrRes},
})
async def get_slide(
    api: SlideApi = Depends(inject_slide_api),
    auth: MyAuth = Security(init_auth, scopes=ScopeType.user_level()),
    # Authorization: str = Header(description='Bearer ...'),
    slide_id: str = Path(),
):
    """
    Response
    - image_url : AWS S3/CloudFront 에서 다운로드(GET) 을 할 수 있는 Presigned URL

    Presigned URL 사용법
     - 다운로드 = HTTP GET https://xxx.cloudfront.net/test.png?Expires=...&Signature=...&Key-Pair-Id=...
    """
    try:
        params = {'slide_id': slide_id}
        res = await api.get_slide(params, auth)
        response = JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(res))
    except HTTPException as e:
        my_logger.error(f"api.get_slide() : e={e.detail}")
        raise e
    except BaseException as e:
        my_logger.error(f"api.get_slide() : e={e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e), headers={'X': 'slide'})
    return response


@router.get("s", summary="슬라이드 리스트 조회", responses={
    200: {"model": SlidesRes},
    401: {"model": ErrRes},
    403: {"model": ErrRes},
    422: {"model": ErrRes},
    500: {"model": ErrRes},
})
async def get_slides(
    api: SlideApi = Depends(inject_slide_api),
    auth: MyAuth = Security(init_auth, scopes=ScopeType.user_level()),
    # Authorization: str = Header(description='Bearer ...'),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1),
    name: str = Query(default=None)
):
    """
    Request
    - name : slide_name 검색 가능.
    - skip&limit : Pagination 가능.
    """
    try:
        params = {'skip': skip, 'limit': limit, 'name': name}
        res = await api.get_slides(params, auth)
        response = JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(res))
    except HTTPException as e:
        my_logger.error(f"api.get_slides() : e={e.detail}")
        raise e
    except BaseException as e:
        my_logger.error(f"api.get_slides() : e={e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e), headers={'X': 'slide'})
    return response


@router.post("", summary="슬라이드 등록 (for upload)", responses={
    200: {"model": SlideRes},
    400: {"model": ErrRes},
    401: {"model": ErrRes},
    403: {"model": ErrRes},
    422: {"model": ErrRes},
    500: {"model": ErrRes},
})
async def post_slide(
    api: SlideApi = Depends(inject_slide_api),
    auth: MyAuth = Security(init_auth, scopes=ScopeType.user_level()),
    # Authorization: str = Header(description='Bearer ...'),
    Content_Type: str = Header(description='application/json'),
    req: SlidePostReq = Body(),
):
    """
    Request
    - slide_name : 임의로 작성.
    - image_name : 확장자를 포함한 파일명. (ex: "test.png")

    Response
    - image_url : AWS S3/CloudFront 에서 업로드(PUT) 을 할 수 있는 Presigned URL

    Presigned URL 사용법
     - 업로드 = HTTP PUT https://xxx.cloudfront.net/test.png?Expires=...&Signature=...&Key-Pair-Id=... (HTTP Body 에 해당 파일첨부)
    """
    try:
        res = await api.post_slide(req, auth)
        response = JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(res))
    except HTTPException as e:
        my_logger.error(f"api.post_slide() : e={e.detail}")
        raise e
    except BaseException as e:
        my_logger.error(f"api.post_slide() : e={e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e), headers={'X': 'slide'})
    return response
