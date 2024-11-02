from dependency_injector import providers

from src.containers import DkDnsContainer, DkTableContainer
from src.core.container import BaseContainer


class Application(BaseContainer):
    DkDnsModule = providers.Container(
        DkDnsContainer
    )
    DkTableModule = providers.Container(
        DkTableContainer
    )
