# FROM python:3.10
# # adicionar a camada que será o diretório padrão a ser utilizado
# WORKDIR /src

# # copiar o arquivo de instalação dos requisitos do ambiente

# RUN apt-get update && apt-get install -y \
#     curl \
#     apt-transport-https \
#     ca-certificates \
#     gnupg \
#     && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
#     && curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list \
#     && apt-get update \
#     && apt-get install -y mssql-tools unixodbc-dev \
#     # Adiciona o diretório onde o sqlcmd é instalado ao PATH
#     && echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc \
#     && source ~/.bashrc

# COPY requirements.txt /src/
# # RUN pip install -r requirements.txt
# RUN pip install --no-cache-dir -r requirements.txt

# # copiar os arquivos da pasta src (source) para diretório padrão do container
# COPY ./app /src/app

FROM python:3.10

# Define o diretório de trabalho
WORKDIR /src

# Instala dependências do sistema e ferramentas necessárias
RUN apt-get update && apt-get install -y \
    curl \
    apt-transport-https \
    ca-certificates \
    gnupg \
    && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y mssql-tools unixodbc-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/* \
    && echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc

# Copia o arquivo de requisitos para o diretório padrão
COPY requirements.txt /src/

# Instala as dependências Python
RUN pip install --no-cache-dir --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt


# Copia os arquivos da aplicação para o diretório de trabalho
COPY ./app /src/app
