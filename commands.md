# FastAPI 프로젝트 초기 설정 명령어 모음

## 프로젝트 실행

docker-compose up --build

## 도커 컨테이너 확인

docker ps

## FastAPI 서버 접속

curl http://localhost:8000/

## 데이터베이스 접속 (PostgreSQL)

docker exec -it fastapi_db psql -U user -d fastapi_db

## 로그 보기

docker logs fastapi_app

## 컨테이너 중지

docker-compose down

## DB 마이그레이션 케이스 생성

alembic revision --autogenerate -m "커밋 메시지"

## DB에 마이그레이션 적용

alembic upgrade head

## 적용된 마이그레이션 되돌리는 명령어

alembic downgrade -1

## 테스트 코드 명령어

PYTHONPATH=. pytest tests
