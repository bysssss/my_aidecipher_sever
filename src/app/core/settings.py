from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AwsSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding='utf-8', extra='ignore')
    profile: str = Field("", alias="AWS_PROFILE")
    config: str = Field("", alias="AWS_CONFIG_FILE")
    credentials: str = Field("", alias="AWS_SHARED_CREDENTIALS_FILE")
    region: str = Field("", alias="AWS_DEFAULT_REGION")
    sss_bucket: str = Field("", alias="AWS_SSS_BUCKET")
    cf_domain: str = Field("", alias="AWS_CF_DOMAIN")
    cf_signer_keyid: str = Field("", alias="AWS_CF_SIGNER_KEYID")


class EtcSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding='utf-8', extra='ignore')
    rsa_private: str = Field("", alias="RSA_PRIVATE")
    rsa_public: str = Field("", alias="RSA_PUBLIC")


class MySettings(BaseSettings):
    my_version: str = ""
    my_stage: str = ""
    my_root: str = ""
    my_name: str = ""
    my_test: str = ""
    my_local: str = ""
    aws: AwsSettings = AwsSettings()
    etc: EtcSettings = EtcSettings()

    def __hash__(self):
        return hash((self.my_version, self.my_stage, self.my_root, self.my_name, self.my_test, self.my_local))


@lru_cache()
def init_my_settings():
    print(f"init_my_settings()")
    return MySettings()


my_settings = MySettings()
print(f"my_settings = {my_settings}")
