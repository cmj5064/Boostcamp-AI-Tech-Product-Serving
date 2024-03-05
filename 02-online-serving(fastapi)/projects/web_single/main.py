from fastapi import FastAPI
from contextlib import asynccontextmanager
from loguru import logger   # python logging을 쉽게 하기 위한 라이브러리 loguru 사용
from sqlmodel import SQLModel

from config import config
from database import engine
from dependencies import load_model
from api import router

# 구현 세번째! Model Load
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 데이터베이스 테이블 생성
    logger.info("Creating database table")
    SQLModel.metadata.create_all(engine)

    # 모델 로드
    logger.info("Loading model")
    load_model(config.model_path)
    # model.py에 존재. 역할을 분리해야 할 수도 있음 (ex. 웹 개발자와 모델러)
    # => 새로운 파일(dependencies.py)을 만들고, 거기서 load_model 구현
    yield # app 구동

app = FastAPI(lifespan=lifespan)
app.include_router(router)

@app.get("/")
def root():
    return "Hello World!"


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    # reload=True: 코드가 변경되면 자동으로 FastAPI Load
    # uvicorn.run(app)이 아닌 uvicorn("main:app")으로 사용