from typing import Optional, List
from pydantic import BaseModel, Field


class _InferenceReq(BaseModel):
    slide_id: int


class InferencePostReq(BaseModel):
    slide: _InferenceReq


class _DensityRes(BaseModel):
    min: float
    avg: float
    max: float


class _InferenceRes(BaseModel):
    inference_id: int = Field(validation_alias='id')
    decision: bool
    score: float
    intratumoral: _DensityRes | None
    stromal: _DensityRes | None


class _InferenceFailRes(BaseModel):
    inference_id: int = Field(validation_alias='id')
    error_message: str


class InferenceRes(BaseModel):
    inference: _InferenceRes | _InferenceFailRes


class InferencesRes(BaseModel):
    inferences: list[_InferenceRes | _InferenceFailRes]
