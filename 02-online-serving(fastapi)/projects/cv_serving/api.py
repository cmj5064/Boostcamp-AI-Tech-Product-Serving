from fastapi import APIRouter, HTTPException, status, UploadFile
from pydantic import BaseModel
from sqlmodel import Session
from PIL import Image
from torchvision.transforms import transforms

from database import PredictionResult, engine
from dependencies import get_model

router = APIRouter()


class PredictionResponse(BaseModel):
    id: int
    result: int


# FastAPI 경로
@router.post("/predict")
def predict(file: UploadFile) -> PredictionResponse:
    # TODO: 이미지 파일과 사이즈가 맞는지 검증

    # TODO: 모델 추론

    # TODO: 결과를 데이터베이스에 저장 (PredictionResult 사용)

    # TODO: 응답하기
    return PredictionResponse(...)
