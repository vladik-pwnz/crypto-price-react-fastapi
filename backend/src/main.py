from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from router import router as router_crypto
from init import init_cmc_client
import asyncio

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    app.state.cmc_client = await init_cmc_client()
    await asyncio.sleep(1)  # Give the client a moment to fully initialize

@app.on_event("shutdown")
async def shutdown_event():
    if hasattr(app.state, 'cmc_client'):
        await app.state.cmc_client.__aexit__(None, None, None)

app.include_router(router_crypto)

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)