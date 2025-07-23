from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from app.routes import router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Libera TUDO. Em produção, restrinja isso!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Inclui as rotas da pasta routes.py
app.include_router(router)

@app.get("/")
def root():
    return {"message": "API Liberty Car rodando 🎉"}

@app.post("/")
async def handle_post(request: Request):
    data = await request.json()  # pega o JSON enviado no corpo da requisição
    # aqui você processa os dados recebidos
    return {"received_data": data}