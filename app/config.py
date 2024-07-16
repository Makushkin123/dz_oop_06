from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # api service settings
    HOST_API: str = "127.0.0.1"
    PORT_API: int = 8080
    MAIN_PREFIX_API: str = "api"
    ADMIN_LOGIN: str = "admin"
    ADMIN_SALT: str = "42"
    SALT: str = "Otus"


settings = Settings()