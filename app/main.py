from fastapi import FastAPI
from concel_data.database import engine
from Schema import model
from routers import posts , users, auth, votes
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(votes.router)