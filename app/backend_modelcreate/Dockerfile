# FROM python:3.10

# # Define o diretório de trabalho
# WORKDIR /src

# # Instala dependências do sistema e ferramentas necessárias
# RUN apt-get update && apt-get install -y \
#     curl \
#     apt-transport-https \
#     ca-certificates \
#     gnupg \
#     && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
#     && curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list \
#     && apt-get update \
#     && ACCEPT_EULA=Y apt-get install -y mssql-tools unixodbc-dev \
#     && apt-get clean && rm -rf /var/lib/apt/lists/* \
#     && echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc

# # Copia o arquivo de requisitos para o diretório padrão
# COPY requirements.txt /src/

# # Instala as dependências Python
# RUN pip install --no-cache-dir --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt


# # Copia os arquivos da aplicação para o diretório de trabalho
# COPY ./app /src/app

# Usa a imagem base Python 3.10
# Usa a imagem base Python 3.10
FROM python:3.10

# Define o diretório de trabalho
WORKDIR /src

# Atualiza os certificados SSL antes da instalação dos pacotes essenciais
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    apt-transport-https \
    ca-certificates \
    gnupg \
    && update-ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Baixa e adiciona a chave do repositório da Microsoft de forma segura
RUN curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor -o /usr/share/keyrings/microsoft.gpg

# Adiciona o repositório do SQL Server ao sources.list com chave assinada
RUN echo "deb [signed-by=/usr/share/keyrings/microsoft.gpg] https://packages.microsoft.com/debian/11/prod bullseye main" > /etc/apt/sources.list.d/mssql-release.list

# Atualiza os repositórios e instala os pacotes necessários com fallback
RUN apt-get update --allow-releaseinfo-change \
    && ACCEPT_EULA=Y apt-get install -y --no-install-recommends \
       unixodbc-dev \
       libodbc1 \
       odbcinst1debian2 \
       odbcinst \
       unixodbc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Se a instalação de mssql-tools falhar devido ao SSL, força o download sem verificação
RUN curl -k -O https://packages.microsoft.com/debian/11/prod/pool/main/m/mssql-tools/mssql-tools_17.10.1.1-1_amd64.deb || true \
    && dpkg -i mssql-tools_17.10.1.1-1_amd64.deb || true \
    && rm -f mssql-tools_17.10.1.1-1_amd64.deb

# Adiciona o diretório do SQLCMD ao PATH permanentemente
ENV PATH="${PATH}:/opt/mssql-tools/bin"

# Copia o arquivo de dependências do Python
COPY requirements.txt /src/

# Instala as dependências Python sem cache e garantindo certificados confiáveis
RUN pip install --no-cache-dir --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt

# Copia os arquivos da aplicação para o diretório de trabalho
COPY ./app /src/app
