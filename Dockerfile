# Usa imagem base leve com Python
FROM python:3.11-slim

# Instala dependências nativas que o WeasyPrint precisa
RUN apt-get update && apt-get install -y \
    build-essential \
    libcairo2 \
    pango1.0-tools \
    libpango1.0-0 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Define diretório de trabalho
WORKDIR /app

# Copia tudo pro container
COPY . .

# Instala dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Expõe a porta do FastAPI
EXPOSE 8000

# Comando pra iniciar o FastAPI com Gunicorn + UvicornWorker
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "main:app", "--bind", "0.0.0.0:8000"]
