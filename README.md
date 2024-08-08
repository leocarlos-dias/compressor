## Execução

Para executar o serviço, siga os passos abaixo:

```bash
docker build -t <image> .
docker run -p 5000:5000 <image>
```

## Rotas

O serviço disponibiliza duas rotas principais:

- `/compress/image`: Recebe uma imagem e retorna sua versão comprimida.
- `/compress/file`: Recebe um arquivo PDF e retorna sua versão comprimida.