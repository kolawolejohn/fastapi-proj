import uvicorn
from fastapi import FastAPI
from database import Base, engine
from core.user.routes import user_router
from core.post.routes import post_router


app = FastAPI()

app.include_router(user_router, prefix="/user")
app.include_router(post_router)

Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    uvicorn.run("app:app", host="localhost", port=8080, reload=True)
