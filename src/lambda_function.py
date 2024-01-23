from main import Main


def lambda_handler(event, lambda_context):
    """

    Author:
        Tensho arai
    """
    try:
        Main(event).exec()
    except Exception as e:
        print(e)


