from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, map, billing

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(map.router, prefix="/map", tags=["map"])
app.include_router(billing.router, prefix="/billing", tags=["billing"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the World Map App API"}