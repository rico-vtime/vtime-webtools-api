from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import share, index, etf, hk

app = FastAPI()
app.include_router(index)
app.include_router(share)
app.include_router(etf)
app.include_router(hk)

origins = [
    "*",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

## uvicorn main:app --host '0.0.0.0' --port 8089 --reload

@app.get("/")
async def read_root():
    return {"Hello": "World"}