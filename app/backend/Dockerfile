# base da imagem Docker a ser utilizada
FROM python:3.10

# adicionar a camada que será o diretório padrão a ser utilizado
WORKDIR /src

# copiar os arquivos da pasta src (source) para diretório padrão do container
COPY ./app /src/modelCreate

# copiar o arquivo de instalação dos requisitos do ambiente
COPY requirements.txt /src

# rodar um comando para instalar os pacotes necessários 
RUN pip install -r requirements.txt

