import time
from fastapi import FastAPI, Request
import grpc
from server import example_pb2, example_pb2_grpc
import pika
import json

from src.post.routers import router as post_router
from src.user.routers import router as user_router
from src.auth.routers import router as auth_router
from src.author.routers import router as author_router
from src.settings.logging_config import logger
from .tasks import register_tasks


def get_application() -> FastAPI:
    _app = FastAPI()
    _app.include_router(post_router)
    _app.include_router(user_router)
    _app.include_router(author_router)
    _app.include_router(auth_router)
    register_tasks(_app)
    return _app


app = get_application()


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time

    logger.info(f"{request.method} {request.url} - {response.status_code} - execution time: {duration:.2f}s")
    return response


@app.get("/hello/{name}", summary='gRPC endpoint')
def say_hello(name: str):
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = example_pb2_grpc.ExampleServiceStub(channel)
        response = stub.SayHello(example_pb2.HelloRequest(name=name))
        return {"message": response.message}


@app.post("/process", summary='RabbitMQ endpoint')
def process(data: dict):
    connection, channel = get_rabbit_channel()

    message = json.dumps(data)
    channel.basic_publish(
        exchange='',
        routing_key='tasks_queue',
        body=message,
        properties=pika.BasicProperties(delivery_mode=2)
    )

    connection.close()

    return {"status": "task sent", "task": data}


def get_rabbit_channel():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters('localhost')
    )
    channel = connection.channel()
    channel.queue_declare(queue='tasks_queue', durable=True)
    return connection, channel
