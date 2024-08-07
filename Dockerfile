# Use uma imagem base oficial do Python
FROM python:3.9-slim

# Defina o diretório de trabalho dentro do container
WORKDIR /app

# Copie o arquivo requirements.txt para o diretório de trabalho
COPY requirements.txt .

# Instale as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copie o restante do código da aplicação para o diretório de trabalho
COPY . .

# Exponha a porta que a aplicação usará
EXPOSE 5000

# Comando para rodar a aplicação usando Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app.main:app"]
