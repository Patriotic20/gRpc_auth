from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select

from core.models.user import User
from core.models.role import Role
from auth.utils.password import verify_password
from auth.schemas.auth import UserRequest

async def get_user(session: AsyncSession , username: str):
    stmt = (
        select(User)
        .where(User.username == username)
        .options(
            selectinload(User.roles).selectinload(Role.permissions)
        ))
    result = await session.execute(stmt)
    return result.scalars().first()

    


async def authenticate_user(session : AsyncSession , user_credential: UserRequest):

    user_data = await get_user(session=session, username=user_credential.username)


    if not user_data:
        return False
    
    if not verify_password(plain_password=user_credential.password, hashed_password=user_data.password):
        return False
    
    return user_data

    
