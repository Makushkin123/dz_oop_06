from typing import Optional, Union, Any
from pydantic import (
    BaseModel,
    Field,
    model_validator,
    field_validator,
)
from .client_interest_request import ClientsInterestsRequest
from .online_score_request import OnlineScoreRequest

from app.config import settings


class MethodRequest(BaseModel):
    account: Optional[str] = Field(None)
    login: str = Field(...)
    token: str = Field(...)
    method: str = Field(...)
    arguments: Union[OnlineScoreRequest, ClientsInterestsRequest] = Field(...)

    @model_validator(mode='before')
    def validate_arguments(cls, values: Any) -> Any:
        method = values.get("method")
        arguments = values.get("arguments")

        if method == "online_score":
            values["arguments"] = OnlineScoreRequest.model_validate(arguments)
        elif method == "clients_interests":
            values["arguments"] = ClientsInterestsRequest.model_validate(arguments)
        else:
            raise ValueError("Invalid method")
        return values

    @field_validator('login')
    def validate_login(cls, value):
        if not value:
            raise ValueError("Поле 'login' обязательно")
        return value

    def is_admin(self):
        return self.login == settings.ADMIN_LOGIN

    def get_empty_fields(self):
        """Возвращает список имен полей, которые имеют значение None."""
        return [field for field, value in self.dict().items() if value is None]

