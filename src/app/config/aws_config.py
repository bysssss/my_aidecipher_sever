from functools import lru_cache

# import boto3
from boto3.session import Session
from botocore.signers import CloudFrontSigner
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding

from app.core.logger import my_logger
from app.core.settings import my_settings


boto_session = Session(
    # region_name=my_settings.aws.region,
    # profile_name=my_settings.aws.profile,
)


@lru_cache()
def init_lambda_client():
    lambda_client = boto_session.client('lambda')
    print(f"init_lambda_client() : lambda_client = {type(lambda_client)}")
    return lambda_client


@lru_cache()
def init_s3_bucket():
    s3 = boto_session.resource('s3')
    s3_bucket = s3.Bucket(my_settings.aws.sss_bucket)
    my_logger.info(f"init_s3_bucket() : s3_bucket = {type(s3_bucket)}")
    return s3_bucket


@lru_cache()
def init_s3_client():
    # config = Config(connect_timeout=3, retries={'max_attempts': 0})
    s3_client = boto_session.client('s3')
    my_logger.info(f"init_s3_client() : s3_client = {type(s3_client)}")
    return s3_client


@lru_cache()
def init_cloudfront_signer():
    cloudfront_signer = CloudFrontSigner(my_settings.aws.cf_signer_keyid, _rsa_signer)
    my_logger.info(f"init_cloudfront_signer() : cloudfront_signer = {type(cloudfront_signer)}")
    return cloudfront_signer


def _rsa_signer(message):
    with open(my_settings.etc.rsa_private, 'rb') as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend()
        )
    return private_key.sign(message, padding.PKCS1v15(), hashes.SHA1())
