"""
coding:utf-8
@Time:2022/8/4 22:40
@Author:XJC
@Description:
"""
import logging
from pathlib import Path
from typing import Optional

from pydantic import Field
# from pydantic import BaseConfig
from pydantic_settings import BaseSettings, SettingsConfigDict

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent


class GlobalSetting(BaseSettings):
    TITLE: str = Field(default='x_one_tool')
    DESCRIPTION: str = Field(default='x_one_tool')
    DEBUG: bool = Field(default=False)
    RELOAD: bool = Field(default=False)
    TIMEZONE: str = Field(default='UTC')
    PORT: int = Field(default=8000)
    HOST: str = Field(default='127.0.0.1')
    LOG_LEVEL: int = Field(default=1)

    MODULE_NAME: str = Field(default='x_one_tool')
    API_V1_STR: str = Field(default='/v1')
    sync_database_url: Optional[str] = Field(default=None)
    database_url: Optional[str] = Field(default=None)
    DB_ECHO_LOG: bool = Field(default=False)
    DB_LOGGING_NAME: str = Field(default='x_one_tool')
    LogPath: str = Field(default='logs')
    model_config = SettingsConfigDict(env_file=(".env", ".env.prod"),
                                      env_file_encoding="utf-8")

settings = GlobalSetting()
