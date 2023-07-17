from apps.common import SQLAlchemyCRUDRouter as CRUDRouter
from apps.db import get_db
from apps.db_catlog.models import (DkDNSType, DkDataSourceinfo, DkCatalogTableRelational, DkCatalogTable, DkCatalog)
from apps.db_catlog.repositories import (DkDnsTypeSchema, DkDnsSchema, DkCatalogTableRelationalSchema,
                                         DkTableSchema, DkCatalogSchema)
from apps.db_catlog.schemas import DkDnsTypeSchemaCreate, DkTableSchemaCreate, DkDnsSchemaCreate

dk_dns_type_router = CRUDRouter(schema=DkDnsTypeSchema, create_schema=DkDnsTypeSchemaCreate, db_model=DkDNSType,
                                db=get_db,
                                update_route=False, delete_all_route=False, delete_one_route=False,
                                tags=["元数据"])
dk_dns_router = CRUDRouter(schema=DkDnsSchema, create_schema=DkDnsSchemaCreate, db_model=DkDataSourceinfo, db=get_db,
                           tags=["数据源"],
                           get_all_route=False, get_one_route=False)

dk_table_router = CRUDRouter(schema=DkTableSchema, create_schema=DkTableSchemaCreate, db_model=DkCatalogTable,
                             db=get_db,
                             get_all_route=False, tags=["表管理"])

dk_catalog_router = CRUDRouter(schema=DkCatalogSchema, db_model=DkCatalog, db=get_db, tags=["目录管理"])

dk_catalog_table_relation = CRUDRouter(schema=DkCatalogTableRelationalSchema, db_model=DkCatalogTableRelational,
                                       db=get_db,
                                       get_one_route=False,
                                       tags=["目录关联管理"])
