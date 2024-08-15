from typing import Optional

from fastapi import APIRouter, Depends, Security, Header, Path, Query, Body, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from app.core.logger import my_logger
from app.config.auth_config import MyAuth, init_auth
from app.common.common_spec import ErrRes
from app.api.inference.inference_api import InferenceApi, inject_inference_api
from app.api.inference.inference_spec import InferencePostReq, InferenceRes, InferencesRes
from app.type.scope_type import ScopeType

router = APIRouter(prefix="/api/v1/inference", tags=["분석 API"])


@router.get("s", summary="분석 이력과 결과 조회", responses={
    200: {"model": InferencesRes},
    401: {"model": ErrRes},
    403: {"model": ErrRes},
    422: {"model": ErrRes},
    500: {"model": ErrRes},
})
async def get_inferences(
    api: InferenceApi = Depends(inject_inference_api),
    auth: MyAuth = Security(init_auth, scopes=ScopeType.user_level()),
    # Authorization: str = Header(description='Bearer ...'),
    slide_id: int = Query(gt=0),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1),
):
    """
    Request
    - slide_id : 조회 대상이되는 슬라이드 아이디.
    - skip&limit : Pagination 가능.
    """
    try:
        params = {'slide_id': slide_id, 'skip': skip, 'limit': limit}
        res = await api.get_inferences(params, auth)
        response = JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(res))
    except HTTPException as e:
        my_logger.error(f"api.get_inferences() : e={e.detail}")
        raise e
    except BaseException as e:
        my_logger.error(f"api.get_inferences() : e={e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e), headers={'X': 'inference'})
    return response


@router.post("", summary="분석 요청", responses={
    200: {"model": InferenceRes},
    400: {"model": ErrRes},
    401: {"model": ErrRes},
    403: {"model": ErrRes},
    422: {"model": ErrRes},
    500: {"model": ErrRes},
})
async def post_inference(
    api: InferenceApi = Depends(inject_inference_api),
    auth: MyAuth = Security(init_auth, scopes=ScopeType.user_level()),
    # Authorization: str = Header(description='Bearer ...'),
    Content_Type: str = Header(description='application/json'),
    req: InferencePostReq = Body(),
):
    """
    Request
    - slide_id : 요청 대상이되는 슬라이드 아이디.
    """
    try:
        res = await api.post_inference(req, auth)
        response = JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(res))
    except HTTPException as e:
        my_logger.error(f"api.post_inference() : e={e.detail}")
        raise e
    except BaseException as e:
        my_logger.error(f"api.post_inference() : e={e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e), headers={'X': 'inference'})
    return response
