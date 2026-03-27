from fastapi import FastAPI
from mangum import Mangum

from chatbot_api.endpoints.v1.routes import router

app = FastAPI(openapi_prefix="/prod")
app.include_router(router, prefix="/v1")

handler = Mangum(app)