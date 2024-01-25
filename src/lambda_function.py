import json
from http import HTTPStatus

from main_bk import Main


def lambda_handler(event, lambda_context):
    """

    Author:
        Tensho arai
    """
    try:
        result: bytes = Main(event).exec()
        response = {
            'statusCode': HTTPStatus.OK,
            'body': json.dumps({'file': result.decode()}),
            'headers': {
                'Content-Type': 'application/json'
            }
        }
        return response
    except Exception as e:
        print(e)
        response = {
            'statusCode': HTTPStatus.INTERNAL_SERVER_ERROR,
            'body': json.dumps({'error': str(e)}),
            'headers': {
                'Content-Type': 'application/json'
            }
        }
        return response


