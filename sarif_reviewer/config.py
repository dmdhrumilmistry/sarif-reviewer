from typing import Optional
from os import getcwd

from pydantic import BaseModel


class Config(BaseModel):
    language: Optional[str] = None
    encoding: Optional[str] = "utf-8"
    logging_level: Optional[str] = "INFO"
    base_dir: Optional[str] = getcwd()


default_config = Config()