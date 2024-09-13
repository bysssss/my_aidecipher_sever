# my_aidecipher_sever

## 구조
    root
    ├── src
    │   ├── app
    │   │   ├── api
    │   │   │   ├── 이름
    │   │   │   │   ├── 이름_router.py
    │   │   │   │   ├── 이름_spec.py
    │   │   │   │   └── 이름_api.py
    │   │   │   └── ...
    │   │   ├── data
    │   │   │   ├── 이름
    │   │   │   │   ├── 이름_schema.py
    │   │   │   │   └── 이름_data.py
    │   │   │   └── ...  
    │   │   ├── core
    │   │   ├── config
    │   │   ├── client
    │   │   ├── aws
    │   │   ├── middleware
    │   │   ├── util
    │   │   ├── type
    │   │   ├── worker
    │   │   │   ├── 이름
    │   │   │   │   └── 이름_worker.py
    │   │   │   └── ...  
    │   │   ├── __init__.py
    │   │   ├── main_api.py
    │   │   └── main_worker.py
    │   ├── resource
    │   │   └── ...
    │   ├── test
    │   │   └── ...
    │   ├── ...
    │   └── requirements.txt
    ├── docker
    │   ├── Dockerfile
    │   └── ...
    ├── secret
    │   ├── aws_config
    │   ├── aws_credentials
    │   └── ...
    ├── .env
    ├── .dockerignore
    ├── docker-compose.yaml
    ├── Makefile
    ├── sam-api-dev.yaml
    ├── sam-worker-dev.yaml
    ├── samconfig.toml
    ├── .gitignore
    └── README.md
---
## Docker 이미지 빌드 
```
pip install -r src/requirements.txt

make build
make build-local

[CircleCI 연동]
l..bs0000@n.com 계정 -> LBS 조직 -> 프로젝트

[DockerHub 연동]
make build-dev
docker tag scp-aislider-app:1.0.0-dev leebs1986/my_aidecipher_server:1.0.0-dev
docker push leebs1986/my_aidecipher_server:1.0.0-dev
```
## 테스트
<img src="doc/upload.png" width="640" height="360">
<img src="doc/download.png" width="640" height="360">
