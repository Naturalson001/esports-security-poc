from fastapi import FastAPI
from api.auth_routes import router as auth_router
from api.training_routes import router as training_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(training_router)