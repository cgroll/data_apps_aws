import json
import pandas

from data_apps_aws.src_data_pipes.fred_data_pipes import update_full_metadata
from data_apps_aws.slack_bots import slack_data_pipe_error, slack_status_update

def lambda_handler(event, context):
    """
    Lambda function to download Fred Metadata and upload to database.
    """

    lambda_func_name = 'FredMetadataFunction'
    data_pipe_logo = "https://www.stlouisfed.org/~/media/Images/Rotator-Images/460x337/Evergreen/Homepage_FRED.jpg"

    start_msg = f'Start data processing for *{lambda_func_name}*'
    print(start_msg)
    slack_status_update(start_msg, data_pipe_logo)

    try:
        update_full_metadata()

        end_msg = f'Data processing successfully done for *{lambda_func_name}*. :heavy_check_mark:'
        print(end_msg)
        slack_status_update(end_msg, data_pipe_logo)

    except:

        print(f'Data processing failed for {lambda_func_name}')
        slack_data_pipe_error('AWS_lambda', lambda_func_name, data_pipe_logo)

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": end_msg,
        }),
    }
