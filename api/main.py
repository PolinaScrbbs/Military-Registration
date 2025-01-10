from fastapi import FastAPI


from .auth.router import router as authRouter
from .content.router import router as contentRouter

app = FastAPI(
    title="Polina's Education",
    description="API for Conducting Practice",
    version="2.2.8",
)


app.include_router(authRouter, tags=["Auth"])
app.include_router(contentRouter, tags=["Content"])
