from sqlalchemy.ext.asyncio import AsyncSession
import auth_pb2_grpc
import auth_pb2

from auth.schemas.auth import UserCreate

from core.models.user import User



class AuthService(auth_pb2_grpc.AuthServiceServicer):
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def Register(self, request, context):
        
        user_data = UserCreate(
            username=request.username,
            password=request.password,
        )
        
        new_user = User(**user_data.model_dump())
        self.session.add(new_user)
        await self.session.commit()
        await self.session.refresh(new_user)
        
        
        return auth_pb2.RegisterReply(
            success = True,
            message=f"User {new_user.username} created successfully"
        )
    
    async def Login(self, request, context):
        pass
    
    async def Refresh(self, request, context):
        pass
    
    async def ValidateToken(self, request, context):
        pass
    
    
    
    
    
