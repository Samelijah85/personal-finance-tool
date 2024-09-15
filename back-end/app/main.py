from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import transactions, budgets, auth, users, reports

app = FastAPI(
    title="Personal Finance Management Tool",
    description="An application for managing personal finances.",
    version="0.1",
    root_path="/api/v1",
)

origins = [
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(transactions.router)
app.include_router(budgets.router)
app.include_router(reports.router)

@app.get("/")
async def read_root():
    return {"message": "Welcome to Personal Finance Management Tool!"}


