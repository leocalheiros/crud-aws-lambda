from lambda_function import saveNota
from custom_encoder import CustomEncoder
def test_saveNota():
    try:
        data_to_save = {
            'nota-id': '2',
            'texto': 'tetestsetsets'
        }

        result = saveNota(data_to_save)

        print(result)
    except Exception as e:
        print(f"Erro durante o teste: {str(e)}")

test_saveNota()