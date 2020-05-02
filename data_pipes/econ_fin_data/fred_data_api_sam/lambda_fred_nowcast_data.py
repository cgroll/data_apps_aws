import json
import pandas

from data_apps_aws.src_data_pipes.fred_data_pipes import update_full_nowcast_data
# import requests

def lambda_handler(event, context):
    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """

    # try:
    #     ip = requests.get("http://checkip.amazonaws.com/")
    # except requests.RequestException as e:
    #     # Send some context about this error to Lambda Logs
    #     print(e)

    #     raise e

    print('Start data processing with new pipeline')
    update_full_nowcast_data()
    print('Data processing done with new pipeline')

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": f"FRED nowcast data updated:",
            # "location": ip.text.replace("\n", "")
        }),
    }
