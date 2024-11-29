from dependency_injector import providers

from src.containers.dk_data import DkDnsContainer, DkTableContainer, DkCatalogContainer
from src.core.container import BaseContainer


class Application(BaseContainer):
    DkDnsModule = providers.Container(
        DkDnsContainer
    )
    DkTableModule = providers.Container(
        DkTableContainer
    )
    DkCatalogModule = providers.Container(
        DkCatalogContainer
    )
