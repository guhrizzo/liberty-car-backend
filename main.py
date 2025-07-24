from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from app.routes import router
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

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

import sys
import os

if getattr(sys, 'frozen', False):
    # Rodando como .exe
    base_path = sys._MEIPASS
else:
    # Rodando como .py normal
    base_path = os.path.abspath(".")

static_folder = os.path.join(base_path, 'static')
print(static_folder)

print("Base Path:", base_path)
print("Static Folder:", static_folder)
print("Conteúdo:", os.listdir(static_folder))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)