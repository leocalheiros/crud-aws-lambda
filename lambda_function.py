import boto3
import os
import logging
import json
from custom_encoder import CustomEncoder

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource("dynamodb")
table_name = 'notas'
table = dynamodb.Table(table_name)

getMethod = 'GET'
postMethod = 'POST'
putMethod = 'PUT'
deleteMethod = 'DELETE'
healthPath = '/health'
notaPath = '/nota'
notasPath = '/notas'


def lambda_handler(event, context):
    logger.info(event)
    httpMethod = event['httpMethod']
    path = event['path']
    if httpMethod == getMethod and path == healthPath:
        response = buildResponse(200)
    elif httpMethod == getMethod and path == notaPath:
        response = getNota(event['queryStringParameters']['notaId'])
    elif httpMethod == getMethod and path == notasPath:
        response = getNotas()
    elif httpMethod == postMethod and path == notaPath:
        response = saveNota(json.loads(event['body']))
    elif httpMethod == putMethod and path == notaPath:
        requestBody = json.loads(event['body'])
        response = modifyNota(requestBody)
    elif httpMethod == deleteMethod and path == notaPath:
        requestBody = json.loads(event['body'])
        response = deleteNota(requestBody['nota-id'])
    else:
        response = buildResponse(404, 'Not Found')
    return response


def getNota(notaId):
    try:
        response = table.get_item(
            Key={
                'nota-id': notaId
            }
        )
        if 'Item' in response:
            return buildResponse(200, response['Item'])
        else:
            return buildResponse(404, {'Message': 'NotaId %s não foi encontrada' % notaId})
    except:
        logger.exception('Erro customizado logger')


def getNotas():
    try:
        response = table.scan()
        result = response['Items']
        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            result.extend(response['Items'])

        body = {
            'notas': result
        }
        return buildResponse(200, body)
    except:
        logger.exception('Erro customizado logger')


def saveNota(requestBody):
    try:
        table.put_item(Item=requestBody)
        body = {
            'Operation': 'SAVE',
            'Message': 'SUCCESS',
            'Item': requestBody
        }
        return buildResponse(200, body)
    except:
        logger.exception('Erro customizado logger')


def modifyNota(requestBody):
    try:
        notaId = requestBody.get('nota-id')
        if notaId is None:
            return buildResponse(400, {'Message': 'Campo "nota-id" é obrigatório para atualização.'})
        response = table.get_item(
            Key={
                'nota-id': notaId
            }
        )

        if 'Item' in response:
            response = table.put_item(Item=requestBody)
            body = {
                'Operation': 'UPDATE',
                'Message': 'SUCCESS',
                'UpdateAttributes': response
            }
            return buildResponse(200, body)
        else:
            return buildResponse(404, {'Message': 'NotaId %s não foi encontrada' % notaId})
    except Exception as e:
        logger.exception('Erro customizado logger: %s' % str(e))
        return buildResponse(500, {'Message': 'Erro interno do servidor.'})


def deleteNota(notaId):
    try:
        # Verifique se a nota existe
        response = table.get_item(
            Key={
                'nota-id': notaId
            }
        )

        if 'Item' not in response:
            return buildResponse(404, {'Message': 'NotaId %s não foi encontrada' % notaId})

        # Verifique se a nota está vazia
        if not response['Item']:
            return buildResponse(400, {'Message': 'NotaId %s está vazia.' % notaId})

        # Exclui a nota
        response = table.delete_item(
            Key={
                'nota-id': notaId
            },
            ReturnValues='ALL_OLD'
        )

        body = {
            'Operation': 'DELETE',
            'Message': 'Success',
            'deletedItem': response
        }
        return buildResponse(200, body)
    except Exception as e:
        logger.exception('Erro customizado logger: %s' % str(e))
        return buildResponse(500, {'Message': 'Erro interno do servidor.'})


def buildResponse(statusCode, body=None):
    response = {
        'statusCode': statusCode,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        }
    }
    if body is not None:
        response['body'] = json.dumps(body, cls=CustomEncoder)
    return response


