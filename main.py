import uvicorn
import logging.config
from app.api import router as api_router
from app.config import settings
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from app.logging_config_service import logging_config_dict_custom

logging.config.dictConfig(config=logging_config_dict_custom)
logger = logging.getLogger(__name__)


# init app
app = FastAPI()
app.include_router(api_router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    error = exc.errors()[0]['type']
    if exc.errors()[0]['type'] == 'missing':
        error = f"{exc.errors()[0]['msg']} field: {exc.errors()[0]['loc'][1]}"
    if exc.errors()[0]['type'] == 'value_error':
        error = str(exc.errors()[0]["ctx"]['error'])
    return JSONResponse(
        status_code=422,
        content={"code": 422, "error": error}
    )


origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    logger.info("start server")
    uvicorn.run(app="main:app", host=settings.HOST_API, port=settings.PORT_API, reload=True)
