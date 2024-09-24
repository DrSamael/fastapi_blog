from fastapi import FastAPI
from post.routers import router as post_router


app = FastAPI()
app.include_router(post_router)
