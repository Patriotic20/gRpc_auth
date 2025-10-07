import asyncio
import logging
from grpc import aio
from auth import auth_pb2_grpc
from auth.service import AuthService
from core.database.db_helper import db_helper
from core.config import LOG_DEFAULT_FORMAT

logging.basicConfig(level=logging.INFO, format=LOG_DEFAULT_FORMAT)
logger = logging.getLogger(__name__)

async def serve():
    logger.info("Starting async gRPC server...")

    server = aio.server()
    auth_pb2_grpc.add_AuthServiceServicer_to_server(AuthService(db_helper), server)

    listen_addr = "[::]:50051"
    server.add_insecure_port(listen_addr)
    logger.info(f"Server listening on {listen_addr}")

    await server.start()
    await server.wait_for_termination()

if __name__ == "__main__":
    asyncio.run(serve())
