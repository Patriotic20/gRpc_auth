import grpc
from concurrent import futures
from auth import auth_pb2_grpc
from auth.service import AuthService
from core.database.db_helper import db_helper

import logging
from core.config import LOG_DEFAULT_FORMAT

# Configure logging once
logging.basicConfig(
    level=logging.INFO,
    format=LOG_DEFAULT_FORMAT
)
logger = logging.getLogger(__name__)


def server():
    logger.info("Starting gRPC server...")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    auth_pb2_grpc.add_AuthServiceServicer_to_server(AuthService(db_helper.session_getter), server)

    listen_addr = "[::]:50051"
    server.add_insecure_port(listen_addr)
    logger.info(f"Server listening on {listen_addr}")

    server.start()
    logger.info("Server started successfully. Waiting for termination...")

    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        logger.info("Server stopped by user interrupt.")


if __name__ == "__main__":
    server()

