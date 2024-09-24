from fastapi import FastAPI
from post.routers import router as post_router

# Create FastAPI app instance
app = FastAPI()

# Include the post routes from routes.py
app.include_router(post_router)
