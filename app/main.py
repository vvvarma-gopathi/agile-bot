from fastapi import FastAPI
from contextlib import asynccontextmanager
from core.models import Base
from core.database import engine,get_db
from auth.auth_routes import auth_router



def health_check():
    return {'status':'ok'}

@asynccontextmanager
async def lifespan(app: FastAPI):
    db=get_db()
    Base.metadata.create_all(bind=engine)
    yield
    print("Server Disconnected successfully")

app = FastAPI(version="1.0.0",title="Agile Bot",description="This is a FastAPI application for Agile Bot",lifespan=lifespan)

@app.get("/")
def root():
    return {"message": "Hello, World!"}
@app.get("/health")
async def health():
    return health_check()

app.include_router(auth_router)