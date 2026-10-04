from pathlib import Path
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent

class JWTSettings(BaseModel):
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        env_nested_delimiter="__",
    )
    db_user: str
    db_password: str
    db_host: str = "127.0.0.1"
    db_port: int = 5432
    db_name: str

    jwt: JWTSettings

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )

    @property
    def jwttoken(self) -> str:
        return (
            f"jwt settings {self.jwt.SECRET_KEY}, {self.jwt.ALGORITHM}, {self.jwt.ACCESS_TOKEN_EXPIRE_MINUTES}"
        )

settings = Settings()

#Для откладки и проверки, что все всё видят
print(settings.database_url)
print(settings.jwttoken)
