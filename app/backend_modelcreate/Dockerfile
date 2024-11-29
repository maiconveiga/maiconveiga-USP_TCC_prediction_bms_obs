# base da imagem Docker a ser utilizada
# FROM python:3.10
FROM python:3.10
# adicionar a camada que será o diretório padrão a ser utilizado
WORKDIR /src

# copiar o arquivo de instalação dos requisitos do ambiente
COPY requirements.txt /src/

# RUN pip install -r requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y curl apt-transport-https
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list
RUN apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql18



# copiar os arquivos da pasta src (source) para diretório padrão do container
COPY ./app /src/app

