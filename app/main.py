from fastapi import FastAPI

from app.core.database import Base, engine
from app.api.routes.url import router, redirect_router


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="URL Shortener API",
    description="A simple URL Shortener built with FastAPI",
    version="1.0.0"
)


app.include_router(router)
app.include_router(redirect_router)


@app.get("/")
def root():
    return {
        "message": "URL Shortener API is running"
    }