from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.main_router import api_router
from app.config.database import sessionmanager
from app.config.init_db import init_db
from app.config.cleanup_db import cleanup_database
from app.config.settings import get_settings
from sqlalchemy import text

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database connection
    sessionmanager.init(settings.DATABASE_URL)
    
    # Initialize database with sample data
    async with sessionmanager.session() as session:
        await init_db(session)
    
    yield
    
    # Cleanup: Clear all tables when shutting down
    if sessionmanager._engine is not None:
        async with sessionmanager.session() as session:
            await cleanup_database(session)
        await sessionmanager.close()

app = FastAPI(lifespan=lifespan)

origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)