from sqlalchemy import Boolean, Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship

from app.config.db_config import DBaseModel


class InferenceSchema(DBaseModel):
    __tablename__ = "tb_inference"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, index=True, nullable=False)
    slide_id = Column(Integer, ForeignKey("tb_slide.id"), index=True, nullable=False)
    decision = Column(Boolean, nullable=False)
    score = Column(Float, nullable=False)

    intratumoral_min = Column(Float)
    intratumoral_avg = Column(Float)
    intratumoral_max = Column(Float)

    stromal_min = Column(Float)
    stromal_avg = Column(Float)
    stromal_max = Column(Float)

    error_message = Column(String)

    def __str__(self) -> str:
        return f"id:{self.id}, user_id:{self.user_id}, slide_id:{self.slide_id}, error_message:{self.error_message}"
