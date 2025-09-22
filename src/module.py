from dependency_injector import providers

from src.dk_data.dk_container import DkDnsContainer, DkTableContainer, DkCatalogContainer
from src.core.container import BaseContainer


class Application(BaseContainer):
    dk_dns = providers.Container(
        DkDnsContainer
    )
    dk_table = providers.Container(
        DkTableContainer
    )
    dk_catalog = providers.Container(
        DkCatalogContainer
    )
