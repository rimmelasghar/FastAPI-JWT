from fastapi import FastAPI,Request,status
from src.auth import router as auth_router


app  = FastAPI(title="FastAPI BoilerPlate OAuth 2.0",docs_url='/docs',version="0.1.0")

app.include_router(auth_router.router)

@app.get("/health",tags=['Default'])
async def get_health():
    return {"message":"Running great like Tikka With Biryani 🚀"}
