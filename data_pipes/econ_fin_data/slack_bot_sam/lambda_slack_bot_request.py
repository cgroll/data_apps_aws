import json
import pandas
import logging

from data_apps_aws.slack_bots import slack_data_pipe_error, slack_status_update

def lambda_handler(event, context):
    """
    Lambda function to respond to slack bot requests.
    """

    lambda_func_name = 'SlackBotFunction'
    logger = logging.getLogger(lambda_func_name)
    data_pipe_logo = "https://www.shareicon.net/data/256x256/2016/01/05/233432_alfred_256x256.png"

    start_msg = f'Start data processing for *{lambda_func_name}*'
    print(start_msg)
    slack_status_update(start_msg, data_pipe_logo)

    try:
        
        print('Hello World')

        end_msg = f'Data processing successfully done for *{lambda_func_name}*. :heavy_check_mark:'
        print(end_msg)
        slack_status_update(end_msg, data_pipe_logo)

    except Exception as e:
        logger.error('Failed lambda function with error: '+ str(e))

        end_msg = f'Data processing failed for {lambda_func_name}'
        print(end_msg)
        print(str(e))
        slack_data_pipe_error('AWS_lambda', lambda_func_name, data_pipe_logo)

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": 'Hello World from new slack bot',
        }),
    }
