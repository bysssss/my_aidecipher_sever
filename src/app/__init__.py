from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder

from app.common.common_spec import ErrRes
from app.middleware.timer_middleware import TimerMiddleware
from app.api.default import default_router
from app.api.slide import slide_router
from app.api.inference import inference_router


def init_router(my_app: FastAPI) -> None:
    my_app.include_router(default_router.router)
    my_app.include_router(slide_router.router)
    my_app.include_router(inference_router.router)


def init_cors(my_app: FastAPI) -> None:
    my_app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["content-disposition"],
    )


def init_middleware(my_app: FastAPI) -> None:
    my_app.add_middleware(TimerMiddleware)
    ...


def init_handler(my_app: FastAPI) -> None:
    async def request_validation_error_handler(request: Request, exc: RequestValidationError):
        method = request.scope.get("method")
        path = request.scope.get("path")

        result = ErrRes(
            err_cd=f"{method} {path} -> app:422",
            err_msg=f"{exc.errors()}"
        )
        return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content=jsonable_encoder(result))

    async def http_exception_handler(request: Request, exc: HTTPException):
        method = request.scope.get("method")
        path = request.scope.get("path")
        resource = exc.headers['X'] if isinstance(exc.headers, dict) and 'X' in exc.headers else 'app'

        result = ErrRes(
            err_cd=f"{method} {path} -> {resource}:{exc.status_code}",
            err_msg=f"{exc.detail}"
        )
        return JSONResponse(status_code=exc.status_code, content=jsonable_encoder(result))

    my_app.add_exception_handler(RequestValidationError, request_validation_error_handler)
    my_app.add_exception_handler(HTTPException, http_exception_handler)
