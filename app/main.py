from  fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from app.profile.route import profile
from app.account.route import account

def create_app() -> FastAPI:
    app = FastAPI(title='Market Place Project1 FastApi', debug=False)
    app.include_router(profile)
    app.include_router(account)
    return app

app = create_app()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(app, port=8000)