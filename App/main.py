import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from fastapi import FastAPI
from User.Routes.User_Router import router as UserRouter

app = FastAPI()
app.include_router(UserRouter)