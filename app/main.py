from fastapi import FastAPI
from contextlib import asynccontextmanager
from auth.models import Base
from core.database import engine,get_db
from auth.auth_routes import auth_router
from projects.routes import project_router
from epics.routes import epic_router
from sprints.routes import sprint_router
from attachments.routes import attachment_router
from fastapi.middleware.cors import CORSMiddleware



def health_check():
    return {'status':'ok'}

@asynccontextmanager
async def lifespan(app: FastAPI):
    db=get_db()
    Base.metadata.create_all(bind=engine)
    yield
    print("Server Disconnected successfully")

app = FastAPI(version="1.0.0",title="Agile Bot",description="This is a FastAPI application for Agile Bot",lifespan=lifespan)

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Hello, World!"}
@app.get("/health")
async def health():
    return health_check()

app.include_router(auth_router)
app.include_router(project_router)
app.include_router(epic_router)
app.include_router(sprint_router)
app.include_router(attachment_router)