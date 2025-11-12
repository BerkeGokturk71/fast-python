from fastapi import FastAPI
from backend.db.base import Base
from backend.db.session import engine
from backend.api.auth import router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Wireguard")

app.include_router(router=router)