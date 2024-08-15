from functools import lru_cache

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.logger import my_logger
from app.core.settings import my_settings
from app.config.auth_config import MyAuth
from app.config.db_config import init_db
from app.data.slide.slide_schema import SlideSchema


class SlideData:
    def __init__(self, db: Session):
        self.db = db
        print(f"init SlideData")

    def __hash__(self):
        return hash(self.db)

    def query_slide(self, slide_id, auth: MyAuth) -> SlideSchema:
        try:
            sql = self.db.query(SlideSchema)
            sql = sql.filter(SlideSchema.user_id == auth.user_id)
            sql = sql.filter(SlideSchema.id == slide_id)

            slide = sql.first()
            my_logger.debug(f"SlideData.query_slide() : slide = {slide}")
        except Exception as e:
            err = f"SlideData.query_slide() : e={e}"
            my_logger.error(err)
            raise HTTPException(status_code=555, detail=err, headers={'X': 'tb_slide'})
        return slide

    def query_slide_list(self, skip, limit, name, auth: MyAuth) -> list[SlideSchema]:
        try:
            sql = self.db.query(SlideSchema)
            sql = sql.filter(SlideSchema.user_id == auth.user_id)
            if name is not None and len(name) > 0:
                sql = sql.filter(SlideSchema.slide_name.contains(name))
            sql = sql.offset(skip).limit(limit)

            slide_list = sql.all()
            if slide_list is None:
                my_logger.info(f"SlideData.query_slide_list() : slide_list is None")
                return []

            my_logger.debug(f"SlideData.query_slide_list() : slide_list = {len(slide_list)}")
        except Exception as e:
            err = f"SlideData.query_slide_list() : e={e}"
            my_logger.error(err)
            raise HTTPException(status_code=555, detail=err, headers={'X': 'tb_slide'})
        return slide_list

    def add_slide(self, slide: SlideSchema) -> SlideSchema:
        try:
            self.db.add(slide)
            self.db.commit()
            self.db.refresh(slide)
            my_logger.debug(f"SlideData.add_slide() : slide = {slide}")
        except Exception as e:
            err = f"SlideData.add_slide() : e={e}"
            my_logger.error(err)
            raise HTTPException(status_code=555, detail=err, headers={'X': 'tb_slide'})
        return slide


@lru_cache()
def inject_slide_data(
        db=Depends(init_db)
):
    print(f"inject_slide_data()")
    return SlideData(db=db)
