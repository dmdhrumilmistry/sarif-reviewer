from typing import Optional
from os import getcwd

from pydantic import BaseModel


class Config(BaseModel):
    language: Optional[str] = None
    encoding: Optional[str] = "utf-8"
    logging_level: Optional[str] = "INFO"
    base_dir: Optional[str] = getcwd()

    ai_base_url: Optional[str] = None
    ai_api_key: Optional[str] = None


default_config = Config()