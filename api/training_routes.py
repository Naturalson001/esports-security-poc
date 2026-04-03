from fastapi import APIRouter
from services.training_service import TrainingService

router = APIRouter()
training_service = TrainingService()


@router.get("/v1/training")
def training():
    training_service.start_training()
    return {"message": "Training completed"}