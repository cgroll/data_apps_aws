import requests
import json

from data_apps_aws.password_manager import get_db_url

jupyter_logo = "https://logodix.com/logo/1741446.png"

def slack_rendering_error(this_nb):

    web_hook_url = get_db_url("slack_bot_webhook")

    slack_msg = {'text': f'Rendering of notebook **{this_nb}** failed. :x:',
                 'image': jupyter_logo,
    }
    requests.post(web_hook_url, data=json.dumps(slack_msg))

def slack_status_update(this_nb):

    web_hook_url = get_db_url("slack_bot_webhook")

    slack_msg = {'text': f'Notebook *{this_nb}* successfully rendered :heavy_check_mark:'}
    requests.post(web_hook_url, data=json.dumps(slack_msg))
    

def main():
    web_hook_url = get_db_url("slack_bot_webhook")

    slack_msg = {'text': 'Message from Python'}

    requests.post(web_hook_url, data=json.dumps(slack_msg))

if __name__ == '__main__':
    main()

