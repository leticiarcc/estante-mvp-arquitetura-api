# Imagem base do Python
FROM python:3.10-slim

#Definição da pasta de trabalho
WORKDIR /app

# Copia e instala as dependências do projeto
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

#Porta no container
EXPOSE 5000

# Comando que inicia o servidor Flask ao rodar o container
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]