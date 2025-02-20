import time
from fastapi import FastAPI, Request

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
