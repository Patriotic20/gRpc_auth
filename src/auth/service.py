import logging
import jwt
from jwt import InvalidTokenError, ExpiredSignatureError
from sqlalchemy.exc import SQLAlchemyError

from auth import auth_pb2, auth_pb2_grpc
from auth.schemas.auth import UserCreate, UserRequest
from auth.utils.authenticate import authenticate_user, get_user
from auth.utils.auth_tokens import create_access_token, create_refresh_token
from core.models.user import User
from core.config import settings, LOG_DEFAULT_FORMAT

# Configure logging
logging.basicConfig(level=logging.INFO, format=LOG_DEFAULT_FORMAT)
logger = logging.getLogger(__name__)


class AuthService(auth_pb2_grpc.AuthServiceServicer):
    def __init__(self, db_helper):
        self.db_helper = db_helper
        logger.info("AuthService initialized with database helper")

    # ---------------------------
    # REGISTER
    # ---------------------------
    async def Register(self, request, context):
        logger.info(f"Register request received for username: {request.username}")

        user_data = UserCreate(username=request.username, password=request.password)
        new_user = User(**user_data.model_dump())

        async with self.db_helper.session_factory() as session:
            try:
                session.add(new_user)
                await session.commit()
                await session.refresh(new_user)

                logger.info(f"User '{new_user.username}' registered successfully.")
                return auth_pb2.RegisterReply(
                    success=True,
                    message=f"User '{new_user.username}' registered successfully."
                )

            except SQLAlchemyError as e:
                await session.rollback()
                logger.error(f"Registration failed for username '{request.username}': {e}")
                return auth_pb2.RegisterReply(
                    success=False,
                    message="Registration failed: internal server error."
                )

    # ---------------------------
    # LOGIN
    # ---------------------------
    async def Login(self, request, context):
        logger.info(f"Login attempt for username: {request.username}")

        user_credentials = UserRequest(username=request.username, password=request.password)

        async with self.db_helper.session_factory() as session:
            user_data = await authenticate_user(session=session, user_credential=user_credentials)

            if not user_data:
                logger.warning(f"Invalid login attempt for username: {request.username}")
                return auth_pb2.LoginReply(
                    access_token="",
                    refresh_token="",
                    error="Invalid username or password"
                )

            token_payload = {"sub": user_data.username}
            access_token = create_access_token(data=token_payload)
            refresh_token = create_refresh_token(data=token_payload)

            logger.info(f"User '{user_data.username}' logged in successfully.")
            return auth_pb2.LoginReply(
                access_token=access_token,
                refresh_token=refresh_token,
                error=""
            )

    # ---------------------------
    # REFRESH TOKEN
    # ---------------------------
    async def Refresh(self, request, context):
        logger.info("Refresh token request received")

        try:
            payload = jwt.decode(
                request.refresh_token,
                settings.jwt.refresh_secret_key,
                algorithms=[settings.jwt.algorithm],
            )

            new_access_token = create_access_token(data={"sub": payload["sub"]})
            logger.info(f"Access token refreshed for user: {payload['sub']}")

            return auth_pb2.RefreshReply(access_token=new_access_token)

        except (InvalidTokenError, ExpiredSignatureError) as e:
            logger.warning(f"Invalid or expired refresh token: {e}")
            context.abort(401, "Invalid or expired refresh token")

    # ---------------------------
    # VALIDATE TOKEN
    # ---------------------------
    async def ValidateToken(self, request, context):
        logger.info("ValidateToken request received")

        try:
            payload = jwt.decode(
                request.token,
                settings.jwt.access_secret_key,
                algorithms=[settings.jwt.algorithm],
            )
            username = payload.get("sub")
            if not username:
                logger.warning("Token missing 'sub' claim")
                return auth_pb2.ValidateTokenReply(valid=False)

        except (InvalidTokenError, ExpiredSignatureError) as e:
            logger.warning(f"Invalid or expired access token: {e}")
            return auth_pb2.ValidateTokenReply(valid=False)

        async with self.db_helper.session_factory() as session:
            user: User | None = await get_user(session=session, username=username)

            if not user:
                logger.warning(f"User not found for username: {username}")
                return auth_pb2.ValidateTokenReply(valid=False)

            roles = user.roles or []
            permissions = list({p.name for role in roles for p in role.permissions})

            logger.info(
                f"Token validated for user: {username}, role: {roles[0].name if roles else None}"
            )

            return auth_pb2.ValidateTokenReply(
                valid=True,
                username=user.username,
                role=roles[0].name if roles else None,
                permissions=permissions
            )
