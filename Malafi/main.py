from fastapi import FastAPI
from . import models
from .database import engine
from .routers import authentication, document

app = FastAPI()

models.Base.metadata.create_all(engine)

app.include_router(document.router)
app.include_router(authentication.router)

