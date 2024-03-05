# 구현 네번째! schema 작성 (PredictionRequest, PredictionResponse)
from pydantic import BaseModel

class PredictionRequest(BaseModel):
    features: list
    # input 데이터를 여러분들의 상황에 맞게 작성

class PredictionResponse(BaseModel):
    id: int
    result: int