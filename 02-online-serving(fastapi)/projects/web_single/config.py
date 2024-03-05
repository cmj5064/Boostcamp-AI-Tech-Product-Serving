# 구현 첫 번째! Config 설정
from pydantic import Field
from pydantic_settings import BaseSettings

class Config(BaseSettings): # pydantic BaseSettings 상속
    db_url: str = Field(default="sqlite:///./db.sqlite3", env="DB_URL")
    model_path: str = Field(default="model.joblib", env="MODEL_PATH")
    app_env: str = Field(default="local", env="APP_ENV")


config = Config()