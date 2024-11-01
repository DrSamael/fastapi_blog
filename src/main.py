from fastapi import FastAPI
from src.post.routers import router as post_router
from src.user.routers import router as user_router
from src.auth.routers import router as auth_router
from src.author.routers import router as author_router


app = FastAPI()
app.include_router(post_router)
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(author_router)
