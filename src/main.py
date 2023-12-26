from fastapi import FastAPI,Request,status
from src.auth import router as auth_router
from src.student import router as student_router

app = FastAPI(
    title="FastAPI with Oauth",
    docs_url='/docs',
    version="0.1.0",
    openapi_url="/openapi.json", 
    servers=[
        {"url": "https://secondapi-0tt2.onrender.com", "description": "Render Development Server"},
        
    ],
)

app.include_router(auth_router.router)
app.include_router(student_router.router)

@app.get("/health",tags=['Default'])
async def get_health():
    return {"message":"Running great like Tikka With Biryani 🚀"}
