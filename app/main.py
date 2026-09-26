# import time

# import psycopg2
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# from psycopg2.extras import RealDictCursor
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

# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres',
#         password='', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connection was successful !!")
#         break
#     except Exception as error:
#         print("Connecting to Database failed")
#         print(f"Error: {error}")
#         time.sleep(2)
    
app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(votes.router)
    