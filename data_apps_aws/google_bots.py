from json import dumps
from httplib2 import Http

from data_apps_aws.password_manager import get_db_url

def main():
    """Hangouts Chat incoming webhook quickstart."""
    url = get_db_url("google_hangouts_bot")

    bot_message = {
        'text' : 'Hello from a Python script!'}

    message_headers = {'Content-Type': 'application/json; charset=UTF-8'}

    http_obj = Http()

    response = http_obj.request(
        uri=url,
        method='POST',
        headers=message_headers,
        body=dumps(bot_message),
    )

    print(response)

if __name__ == '__main__':
    main()
