import dotenv
dotenv.load_dotenv()

from fastapi import FastAPI
from mangum import Mangum

from chatbot_api.endpoints.v1.routes import router



app = FastAPI(
    root_path="/Prod",
)

app.include_router(router, prefix="/v1")

handler = Mangum(app)