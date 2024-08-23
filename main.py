from contextlib import asynccontextmanager
from src.users import user_router, add_super_user
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import uvicorn


@asynccontextmanager
async def lifespan(asgi: FastAPI):
    await add_super_user()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(user_router)

@app.get("/")
async def docs_redirect():
    return RedirectResponse(url="/docs")

if __name__ == '__main__':
    uvicorn.run(app="main:app", reload=True)
