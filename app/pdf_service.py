from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from io import BytesIO
from weasyprint import HTML

app = FastAPI()

@app.post("/pdf")
def gerar_pdf():
    html = "<h1>Teste simples</h1><p>Sem imagens, sem fontes</p>"
    pdf_io = BytesIO()
    HTML(string=html).write_pdf(pdf_io)
    pdf_io.seek(0)
    return StreamingResponse(pdf_io, media_type="application/pdf", headers={"Content-Disposition": "inline; filename=teste.pdf"})
