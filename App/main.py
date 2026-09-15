import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from fastapi import FastAPI
from User.Routes.User_Router import router as UserRouter
from Itens.Routes.Itens_Router import router as ItensRouter

app = FastAPI()
app.include_router(UserRouter, tags=["User"])
app.include_router(ItensRouter, tags=["Itens"])