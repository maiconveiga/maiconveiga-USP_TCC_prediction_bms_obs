from pydantic_settings import BaseSettings
from pydantic import Field

import logging

# Configura o logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Coleta das variáveis de ambiente
class Settings(BaseSettings):
    API_KEY: str = Field(..., env="API_KEY")
    CIDADE: str = Field(..., env="CIDADE")


# Carrega as configurações do aplicativo
settings = Settings()
