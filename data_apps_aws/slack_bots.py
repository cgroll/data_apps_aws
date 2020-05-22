import requests
import json

from data_apps_aws.password_manager import get_db_url

def main():
    web_hook_url = get_db_url("slack_bot_webhook")

    slack_msg = {'text': 'Message from Python'}

    requests.post(web_hook_url, data=json.dumps(slack_msg))

if __name__ == '__main__':
    main()

