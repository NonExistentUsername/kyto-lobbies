from adapters.repository import RamRepository
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from service_player.messagebus import MessageBus
from service_player.unit_of_work import RamUnitOfWork

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
message_bus = MessageBus(RamUnitOfWork(RamRepository()), [], {})


async def get_current_user(uuid: str = Depends(oauth2_scheme)) -> str:
    return uuid


async def get_message_bus() -> MessageBus:
    return message_bus
