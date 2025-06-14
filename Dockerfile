# Base image oficial do Python
FROM python:3.11-slim

# Evita buffer de logs
ENV PYTHONUNBUFFERED=1

# Diretório de trabalho dentro do container
WORKDIR /app

# Copia o requirements antes (melhora cache de build)
COPY requirements.txt .

# Instala as dependências
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copia o restante do código
COPY . .

# Expondo a porta da API (caso queira fazer health checks externos)
EXPOSE 8000

# Comando de inicialização da API
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]