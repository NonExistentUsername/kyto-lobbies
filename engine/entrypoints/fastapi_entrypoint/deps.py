from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(uuid: str = Depends(oauth2_scheme)) -> str:
    return uuid
