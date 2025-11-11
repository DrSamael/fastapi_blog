import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import grpc
from concurrent import futures
import example_pb2_grpc, example_pb2




class ExampleService(example_pb2_grpc.ExampleServiceServicer):
    def SayHello(self, request, context):
        return example_pb2.HelloReply(message=f"Hello, {request.name}!")


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    example_pb2_grpc.add_ExampleServiceServicer_to_server(ExampleService(), server)
    server.add_insecure_port("[::]:50051")
    print("gRPC server started on port 50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
