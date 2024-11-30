FROM python:3.10
# adicionar a camada que será o diretório padrão a ser utilizado
WORKDIR /src

# copiar o arquivo de instalação dos requisitos do ambiente

RUN apt-get update && apt-get install -y \
    curl \
    apt-transport-https \
    ca-certificates \
    gnupg \
    && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && apt-get install -y mssql-tools unixodbc-dev \
    # Adiciona o diretório onde o sqlcmd é instalado ao PATH
    && echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc \
    && source ~/.bashrc

COPY requirements.txt /src/
# RUN pip install -r requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# copiar os arquivos da pasta src (source) para diretório padrão do container
COPY ./app /src/app

