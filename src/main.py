from fastapi import FastAPI
from src.post.routers import router as post_router
from src.user.routers import router as user_router
from src.auth.routers import router as auth_router
from src.author.routers import router as author_router
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
