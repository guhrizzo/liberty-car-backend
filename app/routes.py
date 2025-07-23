from fastapi import APIRouter, Request
from fastapi.responses import FileResponse, JSONResponse
from app.pdf_service import gerar_pdf

router = APIRouter()

@router.post("/gerar-pdf")
async def gerar_pdf_endpoint(request: Request):
    data = await request.json()
    
    nome = data.get("nome")
    cpf = data.get("cpf")
    data_contrato = data.get("dataContrato")
    num_contrato = data.get("numContrato")
    marca = data.get("marca")
    modelo = data.get("modelo")
    placa = data.get("placa")
    valor_fibe = data.get("valorFibe")
    ano_veiculo = data.get("anoVeiculo")
    divida = data.get("divida")
    ipva = data.get("ipva")
    licenciamento = data.get("licenciamento")
    multas = data.get("multas")
    pecas_reparo = data.get("pecasReparo")
    observacao = data.get("observacao")
    proposta = data.get("proposta")
    parcelas_totais = data.get("parcelasTotais")
    parcelas_pagas = data.get("parcelasPagas")
    parcelas_atrasadas = data.get("parcelasAtrasadas")
    valor_pecas_reparadas = data.get("valorPecasReparadas")
    valor_parcela = data.get("valor_parcela")

    # Passa tudo pro serviço que monta o PDF
    pdf_path = gerar_pdf(
    nome, cpf, data_contrato, num_contrato,
    marca, modelo, placa, valor_fibe,
    ano_veiculo, divida, ipva, licenciamento,
    multas, pecas_reparo, observacao, proposta,
    parcelas_totais, parcelas_pagas, parcelas_atrasadas, valor_pecas_reparadas, valor_parcela
)

    return FileResponse(path=pdf_path, filename="proposta.pdf", media_type="application/pdf")
