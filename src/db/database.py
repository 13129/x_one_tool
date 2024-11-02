"""
coding:utf-8
@Time:2022/8/4 22:43
@Author:XJC
@Description:
"""

# Import all the models, so that Base has them before being imported by Alembic

from src.base import DBBaseModel  # noqa: F401
from src.db_catlog.models import DkDnsInfo  # noqa: F401
from src.db_catlog.models import DkCatalogTable  # noqa: F401
from src.db_catlog.models import DkCatalogField  # noqa: F401
from src.db_catlog.models import DkCatalog  # noqa: F401
from src.db_catlog.models import DkDNSType  # noqa: F401
from src.db_catlog.models import DkCatalogTableRelational  # noqa: F401
from src.test.models import DbTestModel  # noqa: F401
