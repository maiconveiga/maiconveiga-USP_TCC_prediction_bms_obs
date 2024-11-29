# base da imagem Docker a ser utilizada
FROM python:3.10

# adicionar a camada que será o diretório padrão a ser utilizado
WORKDIR /src

# copiar o arquivo de instalação dos requisitos do ambiente
COPY requirements.txt /src/requirements.txt

# RUN pip install -r requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# copiar os arquivos da pasta src (source) para diretório padrão do container
COPY ./app /src/app

