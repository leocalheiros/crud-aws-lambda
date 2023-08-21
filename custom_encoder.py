import json
from decimal import Decimal


#essa classe CustomEncoder é usada para criar um codificador personalizado que pode ser passado para a função json.dump() ou json.dumps() como o argumento cls para garantir que objetos Decimal sejam serializados corretamente em JSON.

class CustomEncoder(json.JSONEncoder):    #o dynamoDB vem em decimal, então precisamos fazer ele ser compatível com o JSON
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)      #converter o valor de decimal pra float, que é aceito pra manipular o json

        return json.JSONEncoder.default(self, obj)    #chama o método default da classe pai json.JSONEncoder para lidar com a serialização padrão desse objeto.