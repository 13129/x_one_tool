from dependency_injector import containers, providers

from src.core.container import BaseContainer
from src.repositories import DnsRepository
from src.services import DnsService


class DkDnsContainer(BaseContainer):
    wiring_config = containers.WiringConfiguration(modules=["src.api.v1"])
    repository = providers.Factory(
        DnsRepository,
        session_factory=BaseContainer.db.provided.dk_async_session,
    )
    service = providers.Factory(
        DnsService,
        repository=repository,
    )
