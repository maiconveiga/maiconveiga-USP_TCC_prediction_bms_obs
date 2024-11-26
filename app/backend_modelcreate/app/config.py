from pydantic_settings import BaseSettings
from pydantic import Field

import logging

# Configura o logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
