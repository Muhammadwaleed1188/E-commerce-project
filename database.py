from fastapi import FastAPI
from sqlalchemy import create_engine 
from sqlalchemy.orm import declarative_base , sessionmaker
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
     CORSMiddleware,
     allow_origins=["*"],
     allow_credentials =True,
     allow_methods =["*"],
     allow_headers =["*"]


    
)

app.middleware

DATABASE_URL = "sqlite:///./ecommerce.db" 

engine  = create_engine  (DATABASE_URL,connect_args = {"check_same_thread":False})

Base = declarative_base()

SessionLocal = sessionmaker(autocommit = False,
                            autoflush= False,
                            bind = engine)

def get_db():
    db = SessionLocal()

    try:
         yield db

    finally:
       db.close()

    