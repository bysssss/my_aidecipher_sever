from sqlalchemy import Boolean, Column, Integer, Float, String
from sqlalchemy.orm import relationship

from app.config.db_config import DBaseModel


class SlideSchema(DBaseModel):
    __tablename__ = "tb_slide"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, index=True, nullable=False)
    slide_name = Column(String)
    image_name = Column(String)
    image_path = Column(String)

    def __str__(self) -> str:
        return f"id:{self.id}, user_id:{self.user_id}, slide_name:{self.slide_name}"
