import re
from datetime import datetime
from typing import Optional, Union, Literal
from pydantic import (
    BaseModel,
    field_validator,
    Field,
    model_validator
)
from pydantic_core.core_schema import ValidationInfo


class OnlineScoreRequest(BaseModel):
    first_name: Optional[str] = Field(None)
    last_name: Optional[str] = Field(None)
    email: Optional[str] = Field(None)
    phone: Optional[Union[str, int]] = Field(None)
    birthday: Optional[str] = Field(None)
    gender: Optional[int] = Field(None)

    @field_validator('phone')
    def check_phone(cls, v, info: ValidationInfo) -> Optional[str]:
        if v is None:
            return v

        if isinstance(v, int):
            v = str(v)
        if not v.isdigit():
            raise ValueError(f"Field:{info.field_name} error: The phone doesn't start with 7")
        if len(v) == 11:
            if v[0] == "7":
                return v
            else:
                raise ValueError(f"Field:{info.field_name} error: The phone doesn't start with 7")
        else:
            raise ValueError(f"Field:{info.field_name} error: incorrect number of digits in the phone")

    @field_validator('gender')
    def check_gender(cls, v, info: ValidationInfo) -> Optional[str]:
        if v is None:
            return v
        if v in [0, 1, 2]:
            return v
        else:
            raise ValueError(f"Field:{info.field_name} error: incorrect gender")

    @field_validator('birthday')
    def check_birthday(cls, v, info: ValidationInfo) -> Optional[str]:
        if v is None:
            return v
        try:
            # Парсим строку в объект даты
            v = datetime.strptime(v, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError(f"Field:{info.field_name} error: incorrect format date DD.MM.YYYY")

        # Проверяем, что прошло не больше 70 лет
        years_passed = datetime.today().year - v.year
        if years_passed < 70 and v.year <= datetime.today().year:
            return v
        raise ValueError(f"Field:{info.field_name} error: incorrect date difference is more than 70 years")

    @field_validator('email')
    def check_email(cls, v, info: ValidationInfo) -> Optional[str]:
        email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"

        if v is None:
            return v

        if re.match(email_regex, v):
            return v
        else:
            raise ValueError(f"Field:{info.field_name} error: incorrect email")

    @model_validator(mode='after')
    def check_pair_validate(self):
        pairs = [
            (self.phone, self.email),
            (self.first_name, self.last_name),
            (self.gender, self.birthday)
        ]
        for pair in pairs:
            if not all(pair):
                raise ValueError(f'error: fields is empty')
        return self
