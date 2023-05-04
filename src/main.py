from fastapi import FastAPI
from .models import *
from .routers.users import router as user_router
from .routers.sessions import router as session_router

app = FastAPI(
    docs_url="/api/v2/docs",
    redoc_url="/api/v2/redocs",
    title="Core API",
    description="Analytical Microservice",
    version="1.0",
    openapi_url="/api/v2/openapi.json",
)
app.include_router(user_router)
app.include_router(session_router)

@app.get('/')
async def root():
    return {'message': 'The analytics service is running.'}
