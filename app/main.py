from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.api.api_router import api_router
from fastapi.staticfiles import StaticFiles
from fastapi.security import HTTPBearer
from app.middleware.auth_middleware import auth_middleware
import os
app = FastAPI()
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")

@app.get("/")
async def root():
    return {"message": "API is live"}

@app.middleware("http")
async def add_auth_middleware(request: Request, call_next):
    return await auth_middleware(request, call_next)

if not os.path.exists("uploads"):
    os.makedirs("uploads")

app.mount("/images", StaticFiles(directory="uploads"), name="static")

token_auth_scheme = HTTPBearer()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_credentials= True, 
    allow_methods=['*'],
    allow_headers=["*"]
)

app.include_router(api_router)

# from fastapi import FastAPI, Request
# from fastapi.middleware.cors import CORSMiddleware
# from app.api.api_router import api_router
# from fastapi.staticfiles import StaticFiles
# from fastapi.security import HTTPBearer
# from app.middleware.auth_middleware import auth_middleware
# import os

# app = FastAPI()

# # 1. Clean the Frontend URL (Handle cases where Env Var might be missing)
# FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173").rstrip("/")

# # 2. Root route to fix the "404 Not Found" in logs
# @app.get("/")
# async def root():
#     return {"message": "QuickBite API is running", "docs": "/docs"}


# @app.middleware("http")
# async def add_auth_middleware(request: Request, call_next):
#     return await auth_middleware(request, call_next)


# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=[FRONTEND_URL, "http://localhost:5173"], 
#     allow_credentials=True, 
#     allow_methods=['*'],
#     allow_headers=["*"]
# )

# upload_dir = os.path.join(os.getcwd(), "uploads")
# if not os.path.exists(upload_dir):
#     os.makedirs(upload_dir)

# app.mount("/images", StaticFiles(directory=upload_dir), name="static")

# app.include_router(api_router)

