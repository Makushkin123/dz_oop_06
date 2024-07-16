import logging

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.shemas.score import MethodRequest
from app.utils import check_auth, get_score, get_interests

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

router = APIRouter(tags=["Validation"])


@router.post("/method")
async def get_score_api(method_request: MethodRequest):
    if check_auth(method_request):
        logger.info("user failed to authenticate")
        return JSONResponse(
            status_code=403,
            content={"code": 403, "error": "Forbidden", "has": method_request.get_empty_fields()}
        )

    if method_request.method == "online_score":
        logger.info("get online online_score")
        score = get_score(
            phone=method_request.arguments.phone,
            email=method_request.arguments.email,
            birthday=method_request.arguments.birthday,
            gender=method_request.arguments.gender,
            first_name=method_request.arguments.first_name,
            last_name=method_request.arguments.last_name
        )
        return JSONResponse(
            status_code=200,
            content={"code": 200, "response": {"score": score}}
        )

    if method_request.method == "clients_interests":
        logger.info("get clients_interests")
        client_interest = {}
        for client in method_request.arguments.client_ids:
            client_interest[client] = get_interests()

        return JSONResponse(
            status_code=200,
            content={"code": 200, "response": client_interest}
        )
