from typing import Optional
from pydantic import BaseModel


class ErrRes(BaseModel):
    err_cd: Optional[str]
    err_msg: Optional[str]
