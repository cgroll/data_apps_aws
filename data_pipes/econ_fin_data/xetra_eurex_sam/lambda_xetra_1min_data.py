import json
import pandas

from data_apps_aws.src_data_pipes.deutsche_boerse_1min_data import update_data_in_db, get_delayed_xetra_date_to_process
from data_apps_aws.slack_bots import slack_data_pipe_error, slack_status_update

def lambda_handler(event, context):
    """
    Lambda function to download XETRA and EUREX 1 minute data and upload to database.
    """

    this_date = get_delayed_xetra_date_to_process()
    lambda_func_name = 'XetraOneMinuteFunction'
    data_pipe_logo = "https://www.lynxbroker.de/wp-content/uploads/2019/12/xetra-logo.png"

    start_msg = f'Start data processing for *{lambda_func_name}* and date {this_date}'
    print(start_msg)
    slack_status_update(start_msg, data_pipe_logo)

    try:
        
        update_data_in_db(this_date, 'xetra')

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
