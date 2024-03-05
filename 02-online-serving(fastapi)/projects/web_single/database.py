# 구현 두번째! DB 설정
import datetime
from sqlmodel import SQLModel, Field, create_engine
from config import config


class PredictionResult(SQLModel,table=True):
    id: int = Field(default=None, primary_key=True)
    # primary key: SQL DB에서 특정 기록을 식별하기 위해 사용되는 고유한 id, 기본 키를 부여한다.
    result: int
    created_at: str = Field(default_factory=datetime.datetime.now)
    # default_factory : default를 설정. **동적으로** 값을 지정. 

engine = create_engine(config.db_url)