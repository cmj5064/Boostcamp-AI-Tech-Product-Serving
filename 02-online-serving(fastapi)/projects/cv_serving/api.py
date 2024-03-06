from fastapi import APIRouter, HTTPException, status, UploadFile, File
from pydantic import BaseModel
from sqlmodel import Session
from PIL import Image
from torchvision.transforms import transforms, ToTensor, Normalize
from io import BytesIO

from database import PredictionResult, engine
from dependencies import get_model

router = APIRouter()


class PredictionResponse(BaseModel):
    id: int
    result: int


# FastAPI 경로
@router.post("/predict")
def predict(file: UploadFile = File(...)) -> PredictionResponse:
    # TODO: 이미지 파일과 사이즈가 맞는지 검증 (v)
    if file.content_type != "image/jpeg":
        raise HTTPException(
            detail=f"Wrong format: {file.content_type}", status_code=status.HTTP_404_NOT_FOUND
        )
    if not file.size:
        raise HTTPException(
            detail=f"{file.size} file size", status_code=status.HTTP_404_NOT_FOUND
        )
    image = Image.open(BytesIO(bytearray(file.file.read())))

    # TODO: 모델 추론 (v)
    transform = transforms.Compose([
        ToTensor(),
        Normalize(mean=(0.548, 0.504, 0.497), std=(0.237, 0.247, 0.246))
    ])
    
    image = transform(image).unsqueeze(dim=0)
    image = image.to("cpu")

    model = get_model()
    pred = model(image)
    pred = int(pred.argmax(dim=-1).cpu().numpy())

    # TODO: 결과를 데이터베이스에 저장 (PredictionResult 사용) (v)
    prediction_result = PredictionResult(result=pred)
    with Session(engine) as session:
        session.add(prediction_result)
        session.commit()
        session.refresh(prediction_result)

    # TODO: 응답하기 (v)
    return PredictionResponse(id=prediction_result.id, result=pred)
