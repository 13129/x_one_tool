import logging
import os
import sys
import time
from types import FrameType
from typing import cast, List, Union, Any
from setting import LogPath

from loguru import logger


class Logger:
    """输出日志到文件和控制台"""

    def __init__(self, module_name: str = None, cls_logger=logger, parent_dir: str = None,
                 logs_dir: str = 'logs', level: int = 1):
        # 文件的命名
        parent_dir: str = parent_dir if parent_dir else os.getcwd()
        self._LOGGING_DIR: str = os.path.join(parent_dir, logs_dir)
        if not os.path.isdir(self._LOGGING_DIR):
            os.makedirs(self._LOGGING_DIR)
        self._LOGGING_LEVEL: int = level
        self.levels: List[dict] = []
        self._logger = cls_logger
        self.module_name = module_name

        # log_name = f"Fast_{time.strftime('%Y-%m-%d', time.localtime()).replace('-', '_')}.log"
        # log_path = os.path.join(LogPath, "Fast_{time:YYYY-MM-DD}.log")
        # self.logger = logger
        # # 清空所有设置
        # self.logger.remove()
        # # 判断日志文件夹是否存在，不存则创建
        # if not os.path.exists(LogPath):
        #     os.makedirs(LogPath)
        # 日志输出格式
        # formatter = "{time:YYYY-MM-DD HH:mm:ss} | {level}: {message}"
        # 添加控制台输出的格式,sys.stdout为输出到屏幕;关于这些配置还需要自定义请移步官网查看相关参数说明
        # self.logger.add(sys.stdout,
        #                 format="<green>{time:YYYYMMDD HH:mm:ss}</green> | "  # 颜色>时间
        #                        "{process.name} | "  # 进程名
        #                        "{thread.name} | "  # 进程名
        #                        "<cyan>{module}</cyan>.<cyan>{function}</cyan>"  # 模块名.方法名
        #                        ":<cyan>{line}</cyan> | "  # 行号
        #                        "<level>{level}</level>: "  # 等级
        #                        "<level>{message}</level>",  # 日志内容
        #                 )
        # self.logger.add(log_path,
        #                 level='INFO',
        #                 format='{time:YYYY-MM-DD HH:mm:ss} - '
        #                        "{process.name} | "
        #                        "{thread.name} | "
        #                        '{module}.{function}:{line} - {level} -{message}',
        #                 encoding='utf-8',
        #                 retention=1,
        #                 backtrace=True,
        #                 diagnose=True,
        #                 enqueue=True,
        #                 rotation="100mb",
        #                 compression="zip"
        #                 )

    def add_level(self, name: str, color: str = "<white>", no: int = 0, log_filename: str = ''):
        """Add new logging level to loguru.logger config
        :param name - logging level name
        :param color  - color for logging level
        :param no - minimal logging level
        :param log_filename - filename for current level
        """
        if not log_filename:
            log_filename = f'{self.module_name}-{name}.log'.lower()
        level_data: dict = {
            "config": {"name": name, "color": color},
            "path": os.path.join(self._LOGGING_DIR, log_filename)
        }
        if no:
            level_data["config"].update(no=no)
        if not self._is_level_exists(name):
            self._logger.configure(levels=[level_data["config"]])
        self.levels.append(level_data)

    def _is_level_exists(self, name: str) -> bool:
        level_names = tuple(level.get("config", {}).get("name")
                            for level in self.levels)
        return name in level_names

    def add_logger(self, **kwargs):
        """Add new logging settings to loguru.logger
        :param: More read loguru docs
        """

        level: Union[int, str] = kwargs.get("level", self._LOGGING_LEVEL)
        sink: Any = kwargs.get("sink")
        if not sink:
            sink: str = tuple(
                elem
                for elem in self.levels
                if elem["config"]["name"] == level
            )[0]["path"]
            kwargs.update(sink=sink)
        self.logger.add(**kwargs)

    def log(self, *args, **kwargs):
        return self.logger.log(*args, **kwargs)

    def trace(self, *args, **kwargs):
        return self.logger.trace(*args, **kwargs)

    def catch(self, *args, **kwargs):
        return self.logger.catch(*args, **kwargs)

    def info(self, text, *args, **kwargs):
        return self.logger.info(text, *args, **kwargs)

    def debug(self, text, *args, **kwargs):
        return self.logger.debug(text, *args, **kwargs)

    def error(self, text, *args, **kwargs):
        return self.logger.error(text, *args, **kwargs)

    def warning(self, text, *args, **kwargs):
        return self.logger.warning(text, *args, **kwargs)

    def success(self, text, *args, **kwargs):
        return self.logger.success(text, *args, **kwargs)

    def exception(self, text, *args, **kwargs):
        return self.logger.exception(text, *args, **kwargs)

    def get_new_logger(self):
        """Returns updated loguru.logger instance"""
        return self._logger

    def get_default(self) -> 'Logger':
        """Returns self instance with default settings"""
        self._logger.remove()
        self.add_level("DEBUG", "<white>")
        self.add_level("INFO", "<fg #afffff>")
        self.add_level("WARNING", "<light-yellow>")
        self.add_level("ERROR", "<red>")
        stdout_format = ("{time:YYYY-MM-DD HH:mm:ss}| {process.name} | {thread.name} | "
                         "[{level}] | <cyan>{module}</cyan>.<cyan>{"
                         "function}</cyan>:<cyan>{line}</cyan> | <level>{level}</level>: <level>{message}</level> ")
        self.add_logger(sink=sys.stdout, format=stdout_format, level='DEBUG')
        # self.add_logger(backtrace=True, format=stdout_format, enqueue=True, level='DEBUG', compression="zip",
        #                 rotation="50 MB", retention=10)
        self.add_logger(backtrace=True, format=stdout_format, enqueue=True, level='WARNING', compression="zip",
                        rotation="50 MB",
                        retention=10)
        self.add_logger(backtrace=True, format=stdout_format, enqueue=True, level='ERROR', compression="zip",
                        rotation="50 MB", retention=10)
        info_format = ("{time:YYYY-MM-DD HH:mm:ss} - {process.name} | {thread.name} | [{level}] | "
                       "{module}.{function}:{line} - {level} -{message} ")
        self.add_logger(format=info_format, backtrace=True, enqueue=True,
                        level='INFO', compression="zip", rotation="50 MB", retention=10)
        return self

    @property
    def logger(self):
        return self._logger

    @staticmethod
    def get_logger(module_name: str = 'default', level: int = 20, parent_dir: str = None,
                   logs_dir: str = 'logs'):
        return (
            Logger(module_name=module_name, level=level, parent_dir=parent_dir,
                   logs_dir=logs_dir).get_default().get_new_logger())

    @staticmethod
    def init_config():
        LOGGER_NAMES = ("uvicorn.asgi", "uvicorn.access", "uvicorn")

        # change handler for default uvicorn logger
        logging.getLogger().handlers = [InterceptHandler()]
        for logger_name in LOGGER_NAMES:
            logging_logger = logging.getLogger(logger_name)
            logging_logger.handlers = [InterceptHandler()]


class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:  # pragma: no cover
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = str(record.levelno)

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:  # noqa: WPS609
            frame = cast(FrameType, frame.f_back)
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage(),
        )


Loggers = Logger()
log = Loggers.get_logger(module_name='data_preprocess')
