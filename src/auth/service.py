from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
import auth_pb2_grpc
import auth_pb2 


from auth.schemas.auth import UserCreate
from auth.schemas.auth import UserRequest

from core.models.user import User
from auth.utils.authenticate import authenticate_user

from auth.utils.auth_tokens import (
    create_access_token, 
    create_refresh_token,
    )


class AuthService(auth_pb2_grpc.AuthServiceServicer):
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def Register(self, request, context):    
        user_data = UserCreate(
            username=request.username,
            password=request.password,
        )

        new_user = User(**user_data.model_dump())
        
        try:
            async with self.session.begin():  
                self.session.add(new_user)


            await self.session.refresh(new_user)

            return auth_pb2.RegisterReply(
                success=True,
                message=f"User {new_user.username} created successfully"
            )
        
        except SQLAlchemyError as e:
            await self.session.rollback()  
            return auth_pb2.RegisterReply(
                success=False,
                message=f"Registration failed: {str(e)}"
            )
    
    async def Login(self, request, context):

        user_credential = UserRequest(
            username=request.username,           
            password=request.password,
        )

        user_data = await authenticate_user(session=self.session, user_credential=user_credential)

        if not user_data:
            return auth_pb2.LoginReply(
                error = "Invalid username or password"
            )
            


        token_payload = {"sub": user_data.username}

        access_token = create_access_token(data=token_payload)
        refresh_token = create_refresh_token(data=token_payload)

        return auth_pb2.LoginReply(
            access_token = access_token,
            refresh_token = refresh_token,
        )


    async def Refresh(self, request, context):
        
        pass
    
    async def ValidateToken(self, request, context):
        pass
    
    
    
    
    
