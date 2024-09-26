from fastapi import FastAPI
from post.routers import router as post_router
from user.routers import router as user_router
from auth.routers import router as auth_router


app = FastAPI()
app.include_router(post_router)
app.include_router(user_router)
app.include_router(auth_router)
