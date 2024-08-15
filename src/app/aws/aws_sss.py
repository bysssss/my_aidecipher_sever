from functools import lru_cache

from fastapi import Depends, HTTPException, status

from app.core.logger import my_logger
from app.core.settings import my_settings
from app.config.aws_config import init_s3_client, init_s3_bucket, init_cloudfront_signer
from app.util import time_util


class AwsSss:
    def __init__(self, s3_client, s3_bucket, cloudfront_signer):
        self.s3_client = s3_client
        self.s3_bucket = s3_bucket
        self.cloudfront_signer = cloudfront_signer
        print(f"init AwsSss")

    def __hash__(self):
        return hash((self.s3_client, self.s3_bucket, self.cloudfront_signer))

    def generate_cf_presigned_url(self, s3_key, delta=12):
        try:
            private_url = f"https://{my_settings.aws.cf_domain}/{s3_key}"
            expire_date = time_util.date(delta=delta)
            presigned_url = self.cloudfront_signer.generate_presigned_url(private_url, date_less_than=expire_date)
            my_logger.debug(f"aws_sss.generate_cf_presigned_url() : presigned_url={presigned_url}")
        except Exception as e:
            my_logger.error(f"aws_sss.generate_cf_presigned_url() : e={e}")
            raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(e), headers={'X': 'aws_sss'})
        return presigned_url

    def head(self, s3_key):
        if s3_key is None:
            return None
        bucket = my_settings.aws.sss_bucket
        try:
            header = self.s3_client.head_object(Bucket=bucket, Key=s3_key)
            my_logger.debug(f"aws_sss.head() : header={header}")
        except Exception as e:
            my_logger.info(f"aws_sss.head() : e={e}")
            return None
        return header


@lru_cache()
def inject_aws_sss(
        s3_client=Depends(init_s3_client),
        s3_bucket=Depends(init_s3_bucket),
        cloudfront_signer=Depends(init_cloudfront_signer)
):
    print(f"inject_aws_sss()")
    return AwsSss(s3_client=s3_client, s3_bucket=s3_bucket, cloudfront_signer=cloudfront_signer)
