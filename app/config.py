from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PORTAL_URL: str = "https://portaldatransparencia.gov.br/pessoa/visao-geral"
    TIMEOUT: int = 30


settings = Settings()
