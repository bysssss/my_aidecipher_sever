# scp-aislider-app

## 프로젝트 구조
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
## 1) Docker 이미지 빌드 
```
make build
make build-local
```
## 2) Docker-Compose 시작 및 확인
```
make up
make ps
```
## 3) Swagger 문서 확인 및 테스트
```
http://localhost:5000/docs

3-1) post slide 호출
3-2) 이미지 업로드
3-3) get slides 호출
3-4) get slide 호출
3-5) 이미지 다운로드
3-6) post inference 호출
3-7) get inferences 호출
```
## 3) 이미지 업로드 및 다운로드 (참고)
<img src="doc/upload.png" width="640" height="360">
<img src="doc/download.png" width="640" height="360">

## 4) Docker-Compose 종료
```
make down
```
---
