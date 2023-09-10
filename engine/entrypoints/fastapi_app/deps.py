from factories import create_message_bus, create_uow
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from service_player.messagebus import MessageBus

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
message_bus = create_message_bus(create_uow("ram"))


async def get_current_user(uuid: str = Depends(oauth2_scheme)) -> str:
    return uuid


async def get_message_bus() -> MessageBus:
    return message_bus
