"""
coding:utf-8
@Time:2022/8/4 22:43
@Author:XJC
@Description:
"""

# Import all the models, so that Base has them before being imported by Alembic

from apps.base import BaseModel  # noqa: F401
from apps.db_catlog.models import DkDataSourceInfo  # noqa: F401
from apps.db_catlog.models import DkCatalogTable  # noqa: F401
from apps.db_catlog.models import DkCatalogField  # noqa: F401
from apps.db_catlog.models import DkCatalog  # noqa: F401
from apps.db_catlog.models import DkDNSType  # noqa: F401
from apps.db_catlog.models import DkCatalogTableRelational  # noqa: F401
