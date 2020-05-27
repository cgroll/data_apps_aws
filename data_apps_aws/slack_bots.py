import requests
import json

from data_apps_aws.password_manager import get_db_url

jupyter_logo = "https://logodix.com/logo/1741446.png"
wall_e_img = "https://vignette.wikia.nocookie.net/pixar/images/d/de/Wall%E2%80%A2e_clipped_rev_1.png/revision/latest/scale-to-width-down/310?cb=20170807223723"
fred_st_louis_logo = "https://www.stlouisfed.org/~/media/Images/Rotator-Images/460x337/Evergreen/Homepage_FRED.jpg"

error_channel_id = "C013YGT366S"


# core webhook functions
# - with logo to standard channel
# - with logo to error channel
def slack_status_update(status_msg, service_logo):
    """
    Core function to write message with logo to standard channel via simple webhook
    """

    web_hook_url = get_db_url("slack_webhook")

    slack_msg = {'text': status_msg,
                 'icon_url': service_logo,
    }
    requests.post(web_hook_url, data=json.dumps(slack_msg))
    

def slack_rendering_error(err_msg, service_logo):
    """
    Core function to write message with logo to error channel via simple webhook
    """

    web_hook_url = get_db_url("slack_webhook")
    
    slack_msg = {'text': err_msg,
                 'icon_url': service_logo,
                 'channel': error_channel_id,
    }
    requests.post(web_hook_url, data=json.dumps(slack_msg))


## Data pipe errors
def slack_data_pipe_error(cloud_service, data_pipe_name, data_pipe_logo):
    """
    Message will show which data pipe is affected and also the service (lambda, fargate,...)
    """

    err_msg = f'Error in data pipe *{data_pipe_name}* in service *{cloud_service}* :x:'
    slack_rendering_error(err_msg, data_pipe_logo)


## Jupyter notebook rendering
def jupyter_rendering_error(this_nb):

    err_msg = f'Rendering of notebook *{this_nb}* failed. :x:'
    slack_rendering_error(err_msg, jupyter_logo)


def jupyter_status_update(this_nb):

    status_msg = f'Notebook *{this_nb}* successfully rendered :heavy_check_mark:'
    slack_status_update(status_msg, jupyter_logo)


if __name__ == '__main__':

    lambda_func_name = 'FredMetadataFunction'
    data_pipe_logo = "https://www.stlouisfed.org/~/media/Images/Rotator-Images/460x337/Evergreen/Homepage_FRED.jpg"

    # status update
    start_msg = f'Start data processing for *{lambda_func_name}* '
    slack_status_update(start_msg, data_pipe_logo)

    # error report
    slack_data_pipe_error('AWS_lambda', lambda_func_name, data_pipe_logo)


