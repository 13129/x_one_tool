"""
coding:utf-8
@Time:2022/8/4 22:43
@Author:XJC
@Description:
"""

# Import all the models, so that Base has them before being imported by Alembic

from src.core import DBBaseModel  # noqa: F401
from src.model import DkDataSourcesInfo  # noqa: F401
from src.model import DkTableInfo  # noqa: F401
from src.model import DkTableFieldInfo  # noqa: F401
from src.model import DkCatalog  # noqa: F401
from src.model import DkDataSourcesType  # noqa: F401
from src.model import DkCatalogTableRelational  # noqa: F401