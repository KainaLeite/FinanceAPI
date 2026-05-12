from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from db.base import Base
from db.session import engine
from api.routes import auth, categories, accounts, transaction, transfers, reports, goals, users


def criar_tabelas():
    print("🔥 Criando tabelas...")
    Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def ciclo_de_vida(app: FastAPI):
    criar_tabelas()
    yield


app = FastAPI(lifespan=ciclo_de_vida)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)

app.include_router(categories.router)

app.include_router(accounts.router)

app.include_router(transaction.router)

app.include_router(transfers.router)

app.include_router(reports.router)

app.include_router(goals.router)

app.include_router(users.router)