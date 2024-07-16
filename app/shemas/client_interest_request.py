from datetime import datetime
from typing import Optional, Literal
from pydantic import (
    BaseModel,
    field_validator,
    Field,
)
from pydantic_core.core_schema import ValidationInfo


class ClientsInterestsRequest(BaseModel):
    client_ids: list[int] = Field(...)
    date: Optional[str] = Field(None)

    @field_validator('date')
    def check_date(cls, v, info: ValidationInfo) -> Optional[str]:
        if v is None:
            return v
        try:
            # Парсим строку в объект даты
            v = datetime.strptime(v, "%d.%m.%Y").date()
            return str(v)
        except ValueError:
            raise ValueError(f"Field:{info.field_name} error: incorrect format date DD.MM.YYYY")