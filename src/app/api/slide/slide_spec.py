from typing import Optional, List
from pydantic import BaseModel, Field


class _SlideReq(BaseModel):
    slide_name: str = Field(min_length=2)
    image_name: str = Field(min_length=2)


class SlidePostReq(BaseModel):
    slide: _SlideReq


class _SlideRes(BaseModel):
    slide_id: int = Field(validation_alias='id')
    slide_name: str
    image_name: str
    # image_path: str
    image_url: str | None


class SlideRes(BaseModel):
    slide: _SlideRes


class SlidesRes(BaseModel):
    slides: list[_SlideRes]
