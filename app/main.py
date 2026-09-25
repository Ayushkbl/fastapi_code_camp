import time

import psycopg2
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from psycopg2.extras import RealDictCursor

from .config import settings

# from . import models
# from .database import engine
from .routers import auth, posts, users, votes

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# origins = [
#     "https://www.google.com",
#     "https://www.youtube.com"
# ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres',
        password='', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successful !!")
        break
    except Exception as error:  # noqa: BLE001
        print("Connecting to Database failed")
        print(f"Error: {error}")
        time.sleep(2)
    
app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(votes.router)


if __name__ == "__main__":
    port = settings.port

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
    )




    