from weasyprint import HTML
import os

def gerar_pdf(nome, cpf, data_contrato, num_contrato,
              marca, modelo, placa, valor_fibe,
              ano_veiculo, divida, ipva, licenciamento,
              multas, pecas_reparo, observacao, proposta,
              parcelas_totais, parcelas_pagas, parcelas_atrasadas, valor_pecas_reparadas, valor_parcela):
    
    def format_real(valor):
      return f"R$: {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    
    placa = placa.upper() or "N/A"
    valor_parcela_float = float(valor_parcela or 0)
    valor_pecas_reparo_float = float(valor_pecas_reparadas or 0)

    ipva_float = float(ipva or 0)

    licenciamento_float = float(licenciamento or 0)
    multas_float = float(multas or 0)
    proposta_float = float(proposta or 0)
    valor_fibe_float = float(valor_fibe or 0)

    valor_parcela_fmt = format_real(valor_parcela_float)
    ipva_fmt = format_real(ipva_float)
    licenciamento_fmt = format_real(licenciamento_float)
    multas_fmt = format_real(multas_float)
    valor_pecas_reparo_fmt = format_real(valor_pecas_reparo_float)
    proposta_fmt = format_real(proposta_float)
    valor_fibe_fmt = format_real(valor_fibe_float)

    total_encargos = ipva_float + licenciamento_float + multas_float
    total_encargos_formatado = f"{total_encargos:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    try:
      parcelas_totais = int(parcelas_totais)
      parcelas_pagas = int(parcelas_pagas)
      parcelas_em_atraso = parcelas_totais - parcelas_pagas
      valor_parcela = float(valor_parcela)
    except:
      parcelas_em_atraso = 0
      valor_parcela = 0

    saldo_devedor = parcelas_em_atraso * valor_parcela

    prejuizo = total_encargos + valor_pecas_reparo_float + saldo_devedor

    prejuizo_float = float(prejuizo)

    prejuizo_fmt = format_real(prejuizo_float)


    if saldo_devedor <= 0:
      saldo_devedor_formatado = "Saldo Positivo"
    else:
      saldo_devedor_formatado = f"R$: {saldo_devedor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    bloco_ipva = ""
    bloco_licenciamento = ""
    bloco_multas = ""
    bloco_reparo = ""

    if ipva_float > 0:
      bloco_ipva = f"""
      <div class="dados">
        <p>IPVA atrasado:</p>
        <p class="car-date">{ipva_fmt}</p>
      </div>
      """

    if licenciamento_float > 0:
      bloco_licenciamento = f"""
      <div class="dados">
        <p>Licenciamento:</p>
        <p class="car-date">{licenciamento_fmt}</p>
      </div>
      """

    if multas_float > 0:
      bloco_multas = f"""
      <div class="dados">
        <p>Multas:</p>
        <p class="car-date">{multas_fmt}</p>
      </div>
      """

    if bloco_ipva or bloco_licenciamento or bloco_multas:
      bloco_pendencias = f"""
      <div class="path-line2"></div>
      <h2 class="snd-title">Pendências Adicionais</h2>
      <div class="path-line3"></div>
      {bloco_ipva}
      {bloco_licenciamento}
      {bloco_multas}
      <div class="dados">
        <p>Total de encargos administrativos:</p>
        <p class="car-date">R$: {total_encargos_formatado}</p>
      </div>
      """
    else:
      bloco_pendencias = ""

    if valor_pecas_reparo_float > 0:
      bloco_reparo = f"""
      <h2 class="snd-title">Reparo em Peças</h2>
      <div class="path-line3"></div>
      <div class="dados">
        <p>Peças que precisam de reparo : {pecas_reparo} :</p>
        <p class="car-date">{valor_pecas_reparo_fmt}</p>
      </div>
      """
    

    pasta_base = os.path.abspath("app/static")  # para base_url do PDF

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <style>
        @page {{
        size: A4;
        margin: 0;
        }}

        @font-face {{
          font-family: 'HeadingNowTrial-46Bold';
          src: url('HeadingNowTrial-46Bold.ttf') format('truetype');
          font-weight: bold;
          font-style: normal;
        }}

        @font-face {{
          font-family: 'inter-light';
          src: url('inter-light.otf') format('opentype');
          font-weight: normal;
          font-style: light;
        }}

        @font-face {{
          font-family: 'inter-semi-bold';
          src: url('inter-semi-bold.ttf') format('true type');
          font-weight: 600;
          font-style: normal;
        }}

        @font-face {{
        font-family: 'Inter-medium';
        src: url('Inter-medium.ttf') format('truetype');
        font-weight: 500;
        font-style: normal;
        }}

        html, body {{
          margin: 0;
          margin-left: 0px;
          padding: 0;
          height: 100%;
          width: 100%;
          background-color: #000;
          font-family: 'Arial', sans-serif;
        }}

        .page {{
          page-break-after: always;
          width: 100%;
          height: 100%;
        }}

        .page:last-child {{
          page-break-after: auto;
        }}

        .container {{
          height: 100%;
          width: 100%;
          background-image: url('fundo-1.png');
          background-size: cover;
          background-repeat: no-repeat;
          background-position: center;
          position: absolute;
          margin: 0;
          padding: 0;
        }}

        h1 {{
          z-index: 999 !important;
          text-transform: uppercase;
          font-size: 200px;
          Font-family: 'HeadingNowTrial-46Bold', sans-serif;
          font-weight: bold;
          color: #f2f2f2;
          margin-left: 50px;
          line-height: 0.8;
          margin-bottom: 0px;
          margin-top: 50px;
          text-align: left;
        }}

        h1 span {{
          font-size: 180px;
          color: #f2f2f2;
          margin-bottom: 0px;
          font-weight: bold;
          font-family: 'HeadingNowTrial-46Bold', sans-serif;
        }}

        .seta {{
          margin-left: 50px;
          margin-top: 50px;
          }}

        .date {{
          margin-left: 50px;
          margin-top: 240px;
        }}

        .date p {{
          font-family: 'inter-light', sans-serif;
          color: #f2f2f2;
          font-weight: normal;
          font-size: 22px;
        }}

        .info {{
          display: flex;
          margin-left: 50px;
          gap: 50px;
          color: #f2f2f2;
          }}

        .info .groove {{
          font-family: 'inter-semi-bold', sans-serif;
          font-weight: 600;
          font-size: 26px;
          margin-top: 20px;
        }}

        .client p, .cpf p{{
          font-size: 22px;
          }}

        .logo-blue {{
          position: absolute;
          bottom: 50px;
          left: 50px;
          width: 150px;
        }}

        p {{
          font-size: 18px;
          margin: 5px 0;
          font-family: 'Arial', sans-serif;
          font-weight: normal;
        }}

        .container-2 {{
          position: relative;
          background-image: url('fundo-2.png');
          background-size: cover;
          background-repeat: no-repeat;
          background-position: center;
          display: flex;
          justify-content: center;
          align-items: center;
          width: 100%;
          height: 100%;
          font-family: 'Inter-medium', sans-serif;
        }}

        .subcontainer {{
          width: 85%;
          height: 90%;
          border-radius: 40px;
          display: flex;
          overflow: hidden;
          flex-direction: column;
          justify-content: left;
          background-color: rgba(0, 0, 0, 0.5);
          box-shadow: rgba(26, 20, 19, 0.2) 0px 8px 24px;
        }}

        h2 {{
          font-size: 30px;
          color: #f2f2f2;
          text-align: left;
          margin-left: 50px;
          margin-top: 30px;
          margin-bottom: 18px;
        }}

        .path-line {{
          width: 85%;
          height: 2px;
          background-color: rgba(63, 76, 104, 0.55);
          margin-top: 0px;
          margin-bottom: 20px;
          margin-left: 50px;
          border-radius: 1px;
        }}

        .subcontainer p {{
          margin-left: 50px;
          font-size: 14px;
          color: #e5e5e5;
        }}

        .dados {{
          display: flex;
          flex-direction: row;
          justify-content: space-between;
        }}

        .dados p {{
          color: #e5e5e5;
        }}

        .car-date {{
          margin-right: 50px;
          margin-bottom: 12px;
        }}

        .path-line2 {{
          width: 85%;
          height: 2px;
          background-color: rgba(63, 76, 104, 0.55);
          margin-top: 20px;
          margin-bottom: 10px;
          margin-left: 50px;
          border-radius: 1px;
        }}

        .path-line3 {{
          width: 85%; 
          height: 2px;
          background-color: rgba(63, 76, 104, 0.55);
          margin-top: 5px;
          margin-bottom: 12px;
          margin-left: 50px;
          border-radius: 1px;
        }}

        .snd-title {{
          margin-top: 0px;
          margin-bottom: 10px;
        }}

        .container-3 {{
          position: relative;
          background-image: url('fundo-3.png');
          background-size: cover;
          background-repeat: no-repeat;
          background-position: center;
          width: 100%;
          height: 100%;
          display: flex;
          flex-direction: column;
          align-items: center;
          overflow: hidden;
        }}
        
        .subcontainer-2 {{
          width: 85%;
          height: 92%;
          margin-top: 20px;
          overflow: hidden;
          border-radius: 40px;
          display: flex;
          flex-direction: column;
          justify-content: left;
          background: linear-gradient(180deg,rgba(1, 22, 62, 1) 0%, rgba(0, 0, 0, 1) 100%);
          box-shadow: rgba(26, 20, 19, 0.2) 0px 8px 24px;
        }}

        .thrd-title {{
          font-size: 30px;
          color: #f2f2f2;
          text-align: left;
          font-family: 'Inter-medium', sans-serif;
          margin-left: 50px;
          margin-top: 60px;
          margin-bottom: 18px;
        }}

        .subcontainer-2 p {{
          color: #e5e5e5;
          margin-left: 50px;
        }}

        .car-value {{
          margin-right: 50px;
          font-family: 'Inter-medium', sans-serif;
          font-size: 30px;
          color: #f2f2f2;
          display: flex;
          align-items: center;
        }}

        .prop-comercial {{
          display: flex;
          flex-direction: row;
          justify-content: space-between;
          align-items: start;
        }}

        .prop-comercial p {{
          color: #e5e5e5;
          
        }}

        .text {{
          font-size: 16px;
          color: #e5e5e5;
        }}

        .long-text {{
          font-size: 16px;
          line-height: 1.3;
          color: #e5e5e5;
          margin-top: 20px;
          margin-bottom: 20px;
        }}

        .list {{
          list-style: none;
          padding-left: 0;
          margin-left: 50px;
          color: #e5e5e5;
        }}

        .check {{
          margin: 10px 0;
        }}

        .check li {{
          line-height: 1.5;
        }}

        .condicioes {{
          color: #e5e5e5;
          font-size: 12px;
        }}

        .condicioes p {{
          margin-top: 10px;
          margin-bottom: 10px;
          line-height: 1.5;
          font-size: 15px;
        }}

      </style>
    </head>
    <body>
      <div class="page">
        <div class="container">
          <h1>Proposta </br> <span> Liberty Car</span></h1>
          <img src="seta.png" alt="Seta" class="seta">
          <div class="date">
            <p>{num_contrato}</p>
            <p>{data_contrato}</p>
          </div>
          <div class="info">
            <div class="client">
              <p class="groove">Cliente:</p>
              <p>{nome}</p>
            </div>
            <div class="cpf">
              <p class="groove">CPF:</p>
              <p>{cpf}</p>
            </div>
        </div>
        <img src="logo-liberty-car-blue.png" alt="Logo Liberty Car" class="logo-blue">
        </div>
      </div>
      <div class="page">
        <div class="container-2">
          <div class="subcontainer">
            <h2>Informações do veículo</h2>
            <div class="path-line">
            </div>
            <div class="dados">
              <p>Marca & Modelo:</p>
              <p class="car-date">{marca} / {modelo}</p>
            </div>
            <div class="dados">
              <p>Ano do Veículo:</p>
              <p class="car-date">{ano_veiculo}</p>
            </div>
            <div class="dados">
              <p>Placa do Veículo:</p>
              <p class="car-date">{placa}</p>
            </div>
            <div class="dados">
              <p>Valor de mercado/FIBE:</p>
              <p class="car-date">{valor_fibe_fmt}</p>
            </div>
            <div class="path-line2">
            </div>
            <h2 class="snd-title">Dívida Atual</h2>
            <div class="path-line3">
            </div>
            <div class="dados">
              <p>Parcelas totais:</p>
              <p class="car-date">{parcelas_totais} Parcelas</p>
            </div>
            <div class="dados">
              <p>Parcelas Pagas:</p>
              <p class="car-date">{parcelas_pagas} Parcelas</p>
            </div>
            <div class="dados">
              <p>Parcelas em atraso:</p>
              <p class="car-date">{parcelas_atrasadas} Parcelas</p>
            </div>
            <div class="dados">
              <p>Valor da parcela:</p>
              <p class="car-date">{valor_parcela_fmt}</p>
            </div>
            <div class="dados">
              <p>Saldo devedor total:</p>
              <p class="car-date"> {saldo_devedor_formatado}</p>
            </div>
            <div class="path-line2">
            </div>
            {bloco_pendencias}
            <div class="path-line2">
            </div>
            {bloco_reparo}
          </div>
      </div>
      <div class="page">
        <div class="container-3">
          <div class="subcontainer-2">
            <h2 class="thrd-title">Proposta Comercial</h2>
            <div class="path-line">
            </div>
            <div class="prop-comercial">
              <p class="text">A empresa LibertyCar propõe adquirir o </br> veículo descrito acima por:</p>
              <p class="car-value">{proposta_fmt}</p>
            </div>
            <p class="long-text">Mesmo que o veículo esteja gerando um </br>
                prejuízo acumulado de mais de {prejuizo_fmt} </br>
                a LibertyCar se compromete e assumi todos os </br>
                riscos e responsabilidades do processo, pagando à </br>
                vista por algo que, na prática, está em situação desfavorável.
            </p>
            <p> Este valor inclui os seguintes pontos:</p>
            <ul class="list">
              <div class="check">
              <li><img src="check-blue.png" alt="Check"> Assunção integral da dívida ativa até a quitação total junto ao banco. </li>
              </div>
              <div class="check">
              <li><img src="check-blue.png" alt="Check">Assunção de TODAS as pendências do veículo junto ao Detran </br>
              (IPVA atrasado, multas, licenciamento). </li>
              </div>
              <div class="check">
              <li><img src="check-blue.png" alt="Check"> Assunção dos custos de reparo do veículo (incluindo estética e mecânica).
              Regularização completa da documentação do veículo,  incluindo taxas </br> de
              transferência, vistoria, desbloqueio e o que mais for necessário. </li>
              </div>
              <div class="check">
              <li> <img src="check-blue.png" alt="Check"> Cobertura de eventuais pendências com cartórios (procurações, bloqueios e </br>
              restrições judiciais). </li>
              </div>
              <div class="check">
              <li>
              <img src="check-blue.png" alt="Check">
              Serviço adicional de limpeza de nome, caso a dívida com o banco esteja </br>
              vinculada ao CPF do proprietário. </li>
              </div>
            </ul>
            <h2 class="4th-title">Condições e Garantias</h2>
            <div class="condicioes">
              <p class="2long-text">A proposta é válida por 5 dias a partir da data de emissão deste documento.</p>
              <p class="2long-text">O processo de quitação pode levar de 6 a 12 meses, conforme </br>
              análise do caso e da financeira.
              </p>
              <p class="2long-text">Durante esse período, o cliente não será mais responsável pelo
              pagamento do financiamento, impostos ou multas relacionados ao veículo. </p>
              <p class="2long-text">Após o processo finalizado, nenhuma pendência financeira recairá </br>
              sobre o antigo proprietário</p>
              <p class="2long-text">Um contrato formal será assinado para segurança de
              ambas as partes.</p>
            </div>
            
          </div>
        </div>
      </div>
    </body>
    </html>
    """

    # Salva o HTML para teste no navegador
    with open("teste.html", "w", encoding="utf-8") as f:
        f.write(html_content)

    output_path = "proposta.pdf"
    HTML(string=html_content, base_url=pasta_base).write_pdf(output_path)

    return output_path
