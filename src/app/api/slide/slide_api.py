from functools import lru_cache

from fastapi import Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder

from app.core.logger import my_logger
from app.core.settings import my_settings
from app.config.auth_config import MyAuth
from app.api.slide.slide_spec import SlidePostReq, SlideRes, SlidesRes
from app.data.slide.slide_data import SlideData, inject_slide_data
from app.data.slide.slide_schema import SlideSchema
from app.aws.aws_sss import AwsSss, inject_aws_sss
from app.util import time_util


class SlideApi:
    def __init__(self, slide_data: SlideData, aws_sss: AwsSss):
        self.slide_data = slide_data
        self.aws_sss = aws_sss
        print(f"init SlideApi")

    def __hash__(self):
        return hash((self.slide_data, self.aws_sss))

    async def get_slide(self, params: dict, auth: MyAuth):
        slide_id = f"{params['slide_id']}"
        my_logger.info(f"SlideApi.get_slide() : slide_id={slide_id}")

        slide = self.slide_data.query_slide(slide_id, auth)
        my_logger.info(f"SlideApi.get_slide() : slide={slide}")
        if slide is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"slide is None {params}", headers={'X': 'slide'})

        header = self.aws_sss.head(slide.image_path)
        if header is not None:
            presigned_url = self.aws_sss.generate_cf_presigned_url(slide.image_path, delta=12)
        else:
            presigned_url = None

        slide = jsonable_encoder(slide, custom_encoder={SlideSchema: SlideApi._slide})
        slide['image_url'] = presigned_url
        res = SlideRes(slide=slide)
        return res

    async def get_slides(self, params: dict, auth: MyAuth):
        skip = params['skip']
        limit = params['limit']
        name = params['name']
        my_logger.info(f"SlideApi.get_slide() : skip={skip}, limit={limit}, name={name}")

        slide_list = self.slide_data.query_slide_list(skip, limit, name, auth)
        my_logger.info(f"SlideApi.get_slides() : slide_list={len(slide_list)}")

        slide_list = jsonable_encoder(slide_list, custom_encoder={SlideSchema: SlideApi._slide})
        for slide in slide_list:
            presigned_url = self.aws_sss.generate_cf_presigned_url(slide['image_path'])
            slide['image_url'] = presigned_url
        res = SlidesRes(slides=slide_list)
        return res

    async def post_slide(self, req: SlidePostReq, auth: MyAuth):
        user_id = f"{auth.user_id}"
        my_logger.info(f"SlideApi.post_slide() : user_id={user_id}")

        image_name = req.slide.image_name
        ext_list = image_name.split('.')
        if len(ext_list) < 2:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Bad Extension {image_name}", headers={'X': 'slide'})
        ext = ext_list[-1].lower()

        s3_key = f"scp/{user_id}/img.{time_util.timestamp()}.{ext}"
        presigned_url = self.aws_sss.generate_cf_presigned_url(s3_key)

        slide = SlideSchema(
            user_id=user_id,
            slide_name=req.slide.slide_name,
            image_name=req.slide.image_name,
            image_path=s3_key
        )
        slide = self.slide_data.add_slide(slide)
        my_logger.info(f"SlideApi.post_slide() : slide={slide}")

        slide = jsonable_encoder(slide, custom_encoder={SlideSchema: SlideApi._slide})
        slide['image_url'] = presigned_url
        res = SlideRes(slide=slide)
        return res

    @staticmethod
    def _slide(obj: SlideSchema) -> dict:
        return {
            'id': obj.id,
            "slide_name": obj.slide_name,
            "image_name": obj.image_name,
            "image_path": obj.image_path,
            "image_url": None,
        }


@lru_cache()
def inject_slide_api(
        slide_data: SlideData = Depends(inject_slide_data),
        aws_sss: AwsSss = Depends(inject_aws_sss),
):
    print(f"inject_slide_api()")
    return SlideApi(slide_data=slide_data, aws_sss=aws_sss)
