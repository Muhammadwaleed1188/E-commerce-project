from fastapi import FastAPI

from .database import Base, engine

from .routers import cart
from .routers import auth
from .routers import products


from fastapi.middleware.cors import CORSMiddleware


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Task Management API"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500", "http://localhost:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(cart.router)
app.include_router(auth.router)
app.include_router(products.router)


@app.get("/")
def root():
    return {
        "message": "Task Management API is running"
    }