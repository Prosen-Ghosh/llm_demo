from fastapi import FastAPI
from dotenv import load_dotenv
from .routers import health, users, enrich

load_dotenv()

app = FastAPI(title="profile-enricher", version="0.1.0")
app.include_router(health.router, tags=['health'])
app.include_router(users.router, tags=['users'])
app.include_router(enrich.router, tags=['dummy-enrich'])


