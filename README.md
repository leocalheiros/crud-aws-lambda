  ## Endpoints da API:
- GET https://diy0zbu363.execute-api.us-east-2.amazonaws.com/prod/notas/ - retorna a lista de notas
- GET https://diy0zbu363.execute-api.us-east-2.amazonaws.com/prod/health - verifica se a api está retornando
- POST https://diy0zbu363.execute-api.us-east-2.amazonaws.com/prod/nota - criar nota. 
- JSON para criar nota:
{
    "nota-id": "numernovo",
    "texto": "texto"
}

- DELETE https://diy0zbu363.execute-api.us-east-2.amazonaws.com/prod/nota - deleta nota no nota-id
- JSON para DELETE:
{
    "nota-id": ""
}

- PUT https://diy0zbu363.execute-api.us-east-2.amazonaws.com/prod/nota - modifyNota() :
- JSON para PUT:
{
    "nota-id": "notajaexistente",
    "texto": "campo aqui"
}
