from functools import lru_cache
import random

from fastapi import Depends

from app.core.logger import my_logger
from app.core.settings import my_settings
from app.config.auth_config import MyAuth
from app.data.inference.inference_data import InferenceData, inject_inference_data
from app.data.inference.inference_schema import InferenceSchema
from app.util import time_util


class InferenceWorker:
    def __init__(self, inference_data: InferenceData):
        self.inference_data = inference_data
        print(f"init InferenceWorker")

    def post_inference(self, user_id, slide_id) -> InferenceSchema:
        my_logger.info(f"InferenceWorker.post_inference() : user_id={user_id}, slide_id={slide_id}")

        inference = InferenceSchema(
            user_id=user_id,
            slide_id=slide_id,
            decision=random.choice([True, False]),
            score=random.randint(0, 10)*0.1,
            intratumoral_min=0.1,
            intratumoral_avg=0.2,
            intratumoral_max=0.3,
            stromal_min=-0.3,
            stromal_avg=-0.2,
            stromal_max=-0.1,
            error_message=random.choice([None, None, 'test error message'])
        )
        inference = self.inference_data.add_inference(inference)
        my_logger.info(f"SlideApi.post_slide() : inference={inference}")

        return inference


@lru_cache()
def inject_inference_worker(
        inference_data: InferenceData = Depends(inject_inference_data),
):
    print(f"inject_inference_worker()")
    return InferenceWorker(inference_data=inference_data)
