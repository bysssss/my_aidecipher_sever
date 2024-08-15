from functools import lru_cache

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.logger import my_logger
from app.core.settings import my_settings
from app.config.auth_config import MyAuth
from app.config.db_config import init_db
from app.data.inference.inference_schema import InferenceSchema


class InferenceData:
    def __init__(self, db: Session):
        self.db = db
        print(f"init InferenceData")

    def __hash__(self):
        return hash(self.db)

    def query_inference_list(self, slide_id, skip, limit, auth: MyAuth) -> list[InferenceSchema]:
        try:
            sql = self.db.query(InferenceSchema)
            sql = sql.filter(InferenceSchema.user_id == auth.user_id)
            sql = sql.filter(InferenceSchema.slide_id == slide_id)
            sql = sql.offset(skip).limit(limit)

            inference_list = sql.all()
            if inference_list is None:
                my_logger.info(f"InferenceData.query_inference_list() : inference_list is None")
                return []

            my_logger.debug(f"InferenceData.query_inference_list() : inference_list = {len(inference_list)}")
        except Exception as e:
            err = f"InferenceData.query_inference_list() : e={e}"
            my_logger.error(err)
            raise HTTPException(status_code=555, detail=err, headers={'X': 'tb_inference'})
        return inference_list

    def add_inference(self, inference: InferenceSchema) -> InferenceSchema:
        try:
            self.db.add(inference)
            self.db.commit()
            self.db.refresh(inference)
            my_logger.debug(f"InferenceData.add_inference() : inference = {inference}")
        except Exception as e:
            err = f"InferenceData.add_inference() : e={e}"
            my_logger.error(err)
            raise HTTPException(status_code=555, detail=err, headers={'X': 'tb_inference'})
        return inference


@lru_cache()
def inject_inference_data(
        db=Depends(init_db)
):
    print(f"inject_inference_data()")
    return InferenceData(db=db)
