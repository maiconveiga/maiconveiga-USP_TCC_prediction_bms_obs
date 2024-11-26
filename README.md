# TCC - Maicon Veiga

### Subindo o Ambiente do Elastic Stack ELK

1. **Crie um diretório para armazenar os dados do Elasticsearch:**

    ```bash
    mkdir elasticsearch_data
    ```

2. **Inicie os containers definidos no arquivo `docker-compose.yml` na raiz do projeto, em modo desacoplado (`-d`) e reconstruindo as imagens se necessário (`--build`):**

    ```bash
   docker compose up -d
    ```
### Portas

1. Weave Scope http://localhost:4040
2. Frontend http://localhost:3000
3. Backend app http://localhost:8000
4. Backend model_create http://localhost:8001
5. App NGINX http://localhost:9001
6. create_movel NGINX http://localhost:9001/train
7. Kibana http://localhost:5601/
### Possíveis erros


1. Caso os logs do filebeat não estejam sendo coletados no nginx:

    Acesse o container do nginx executando:
    ```bash
    docker exec -it nginx bash
    ```
    Verifique se o filebeat está rodando:
    ```bash
    service filebeat status
    ```
    Caso ele não esteja rodando e apresentando uma mensagem de erro, execute o seguinte comando:
    ```bash
    service filebeat restart
    ```