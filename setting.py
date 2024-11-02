"""
coding:utf-8
@Time:2022/8/4 22:40
@Author:XJC
@Description:
"""
import logging
import os
from enum import Enum
from functools import lru_cache
from pathlib import Path
from typing import Optional

# from pydantic import BaseConfig
from pydantic_settings import BaseSettings, SettingsConfigDict

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent


class GlobalSetting(BaseSettings):
    TITLE: str
    DESCRIPTION: str
    DEBUG: bool
    RELOAD: bool
    TIMEZONE: str
    PORT: int
    HOST: str
    LOG_LEVEL: int

    MODULE_NAME: str
    API_V1_STR: str
    sync_database_url: Optional[str]
    database_url: Optional[str]
    DB_ECHO_LOG: bool
    DB_LOGGING_NAME: str
    LogPath: str
    model_config = SettingsConfigDict(env_file=(".env", ".env.prod"),
                                      env_file_encoding="utf-8")


# class EnvironmentEnum(str, Enum):
#     PRODUCTION = "production"
#     LOCAL = "local"

# class GlobalConfig(BaseConfig):
#     TITLE: str = "DBTool"
#     DESCRIPTION: str = "DB工具"
#     ENVIRONMENT: EnvironmentEnum
#     DEBUG: bool = True
#     RELOAD: bool = True
#     TESTING: bool = False
#     TIMEZONE: str = "UTC"
#     LOG_LEVEL: int = 1
#     MODULE_NAME: str = 'x_one_tool'
#     # Api V1 prefix
#     API_V1_STR = "/v1"
#     # DATABASE_URL: Optional[FilePath] = os.path.join(BASE_DIR, "db.sqlite3")
#     DATABASE_URL: Optional[str] = None

#     DB_ECHO_LOG: bool = False
#     DB_LOGGING_NAME: str = 'DBTool'
#     LogPath = 'logs'

#     @property
#     def sync_database_url(self) -> Optional[str]:
#         # self.DATABASE_URL = "postgresql+psycopg2://zhsq:zhsq@192.168.30.66/x_one_tool"
#         # self.SYNC_DATABASE_URL = "postgresql://postgres:8693585@192.168.3.101/data_preprocess"
#         # return self.DATABASE_URL if self.DATABASE_URL else self.DATABASE_URL
#         self.DATABASE_URL = "sqlite:///{}/db.sqlite3".format(BASE_DIR)
#         return self.DATABASE_URL if self.DATABASE_URL else self.DATABASE_URL

#     class Config:
#         case_sensitive = True

# class LocalConfig(GlobalConfig):
#     """Local configurations."""

#     DEBUG: bool = True
#     ENVIRONMENT: EnvironmentEnum = EnvironmentEnum.LOCAL

# class ProdConfig(GlobalConfig):
#     """Production configurations."""

#     DEBUG: bool = False
#     ENVIRONMENT: EnvironmentEnum = EnvironmentEnum.PRODUCTION

# class FactoryConfig:
#     def __init__(self, environment: Optional[str]):
#         self.environment = environment

#     def __call__(self) -> GlobalConfig:
#         if self.environment == EnvironmentEnum.LOCAL.value:
#             return LocalConfig()
#         return ProdConfig()

# @lru_cache()
# def get_configuration() -> GlobalConfig:
#     return FactoryConfig(os.environ.get("ENVIRONMENT"))()

settings = GlobalSetting()
