from functools import lru_cache

from fastapi import Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder

from app.core.logger import my_logger
from app.core.settings import my_settings
from app.config.auth_config import MyAuth
from app.api.inference.inference_spec import InferencePostReq, InferenceRes, InferencesRes
from app.data.inference.inference_data import InferenceData, inject_inference_data
from app.data.inference.inference_schema import InferenceSchema
from app.worker.inference.inference_worker import InferenceWorker, inject_inference_worker
from app.util import time_util


class InferenceApi:
    def __init__(self, inference_data: InferenceData, inference_worker: InferenceWorker):
        self.inference_data = inference_data
        self.inference_worker = inference_worker
        print(f"init InferenceApi")

    def __hash__(self):
        return hash((self.inference_data, self.inference_worker))

    async def get_inferences(self, params: dict, auth: MyAuth):
        slide_id = params['slide_id']
        skip = params['skip']
        limit = params['limit']
        my_logger.info(f"InferenceApi.get_inferences() : slide_id={slide_id}, skip={skip}, limit={limit}")

        inference_list = self.inference_data.query_inference_list(slide_id, skip, limit, auth)
        my_logger.info(f"InferenceApi.get_inferences() : inference_list={len(inference_list)}")

        inference_list = jsonable_encoder(inference_list, custom_encoder={InferenceSchema: InferenceApi._inference})
        res = InferencesRes(inferences=inference_list)
        return res

    async def post_inference(self, req: InferencePostReq, auth: MyAuth):
        user_id = f"{auth.user_id}"
        slide_id = req.slide.slide_id
        my_logger.info(f"InferenceApi.post_inference() : user_id={user_id} slide_id={slide_id}")

        # payload = {
        #     'case': 'post_inference',
        #     'user_id': user_id,
        #     'slide_id': slide_id,
        # }
        # self.aws_lambda.invoke(f"{my_settings.aws.lambda_func}", 'Event', payload)
        inference = self.inference_worker.post_inference(user_id, slide_id)

        inference = jsonable_encoder(inference, custom_encoder={InferenceSchema: InferenceApi._inference})
        res = InferenceRes(inference=inference)
        return res

    @staticmethod
    def _inference(obj: InferenceSchema) -> dict:
        if obj.error_message is not None:
            return {'id': obj.id, 'error_message': obj.error_message}
        return {
            'id': obj.id,
            "decision": obj.decision,
            "score": obj.score,
            "intratumoral": {
                'min': obj.intratumoral_min,
                'avg': obj.intratumoral_avg,
                'max': obj.intratumoral_max,
            },
            "stromal": {
                'min': obj.stromal_min,
                'avg': obj.stromal_avg,
                'max': obj.stromal_max,
            }
        }


@lru_cache()
def inject_inference_api(
        inference_data: InferenceData = Depends(inject_inference_data),
        inference_worker: InferenceWorker = Depends(inject_inference_worker),
):
    print(f"inject_inference_api()")
    return InferenceApi(inference_data=inference_data, inference_worker=inference_worker)
