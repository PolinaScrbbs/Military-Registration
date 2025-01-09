from fastapi import FastAPI


from .auth.router import router as authRouter

app = FastAPI(
    title="Polina's Education",
    description="API for Conducting Practice",
    version="2.2.8",
)


app.include_router(authRouter, tags=["Auth"])
