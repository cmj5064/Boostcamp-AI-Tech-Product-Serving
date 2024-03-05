from fastapi import APIRouter, HTTPException, status
from schemas import PredictionRequest, PredictionResponse
from dependencies import get_model
from database import PredictionResult, engine
from sqlmodel import Session, select

router = APIRouter() # tag api 그룹을 지어주기 위함

# 구현 네번째! Post /predict
# Request를 input으로 예측을 진행하고, Response를 반환, DB에 저장
@router.post("/predict")
def predict(request: PredictionRequest) -> PredictionResponse:
    # 모델 load
    model = get_model()    
    
    # 예측 : 여러분들의 코드 상황에 따라 구현
    prediction = int(model.predict([request.features])[0])
     
    # 구현 다섯번째! 예측한 결과(Response)를 DB에 저장
    prediction_result = PredictionResult(result=prediction) # 데이터베이스에 저장할 객체를 schema response로 생성. 그 때 prediction을 사용
    with Session(engine) as session:    # 예측한 결과를 DB에 저장
        session.add(prediction_result)
        session.commit()
        session.refresh(prediction_result)

    return PredictionResponse(id=prediction_result.id, result=prediction)

    # return PredictionResponse

# 구현 여섯번째! GET /predict
# DB에 저장된 모든 PredictionResponse를 반환
@router.get("/predict")
def get_predictions() -> list[PredictionResponse]: # 결과 list로 반환
    with Session(engine) as session:
        # prediction_results = session.query(PredictionResult).all()
        # query(result).all()은 deprecate 예정. 대신 아래 두 줄과 같이 select로 대체
        statement = select(PredictionResult)
        prediction_results = session.exec(statement).all()
        return [
            PredictionResponse(id=prediction_result.id, result=prediction_result.result)
            for prediction_result in prediction_results
        ]

# 구현 마지막! GET /predict/{id}
# id로 필터링해서, 해당 id에 맞는 PredictionResponse를 반환
@router.get("/predict/{id}")
def get_preidction(id: int) -> PredictionResponse:
    with Session(engine) as session:
        prediction_result = session.get(PredictionResult, id)
        if not prediction_result:   # result가 없는 경우 error handling
            raise HTTPException(
                detail="Not found", status_code=status.HTTP_404_NOT_FOUND
            )
        return PredictionResponse(
            id=prediction_result.id, result=prediction_result.result
        )

