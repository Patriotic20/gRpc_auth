import grpc
from concurrent import futures
from auth import auth_pb2_grpc
from auth.service import AuthService


def server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    auth_pb2_grpc.add_AuthServiceServicer_to_server(AuthService(), server)
    
    server.add_insecure_port("[::50051]")
    server.start()
    
    server.wait_for_termination()
    
    
if __name__ =="__main__":
    server()
    
    
