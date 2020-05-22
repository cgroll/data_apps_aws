import os

IS_DEPLOYED = os.getenv('IS_DEPLOYED', "False")

if IS_DEPLOYED == "True":

    db_connections = {

        'quandl': {'user': os.getenv('quandl_user', 'NOT_DEFINED'),
                   'api_token': os.getenv('quandl_api_token', 'NOT_DEFINED')
                   },

        'fred': {'api_token': os.getenv('fred_api_token', 'NOT_DEFINED')
                 },

        'slack_bot_webhook': {'url': os.getenv('slack_bot_webhook', 'NOT_DEFINED_YET')
                 },

        "econ_data": {"user": os.getenv('econ_data_user', 'NOT_DEFINED_USER'),
                      "password": os.getenv('econ_data_password', 'NOT_DEFINED_PWD'),
                      "url": os.getenv('econ_data_url', 'NOT_DEFINED_URL'),
                      },

        "econ_data_read": {"user": os.getenv('econ_data_read_user', 'NOT_DEFINED_USER'),
                           "password": os.getenv('econ_data_read_password', 'NOT_DEFINED_PWD'),
                           "url": os.getenv('econ_data_read_url', 'NOT_DEFINED_URL'),
                           },
    }


    def get_api_token(db_name):
        return db_connections[db_name]['api_token']


    def get_db_url(db_name):
        return db_connections[db_name]['url']


    def get_db_password(db_name):
        return db_connections[db_name]['password']


    def get_db_user(db_name):
        return db_connections[db_name]['user']

else:

    import sys
    from data_apps_aws.paths import ProjectPaths

    try:
        
        sys.path.append(str(ProjectPaths.secret_path))
        import passwords.secrets as secrets

    except ImportError:
        print('The import of database passwords did not work.\n' +
              f'Please add file secrets.py into directory {str(ProjectPaths.passwords_path)}')

        place_holder_example = """
        db_connections = {
            'econ-fin-data': {'user': 'username',
                             'password': 'FILL_IN_PASSWORD_HERE',
                             'url': 'some_aws_address'
            },
        }
        """

        print('The content of the file should look like this:')
        print(place_holder_example)


    def get_api_token(db_name):
        return secrets.db_connections[db_name]['api_token']


    def get_db_url(db_name):
        return secrets.db_connections[db_name]['url']


    def get_db_password(db_name):
        return secrets.db_connections[db_name]['password']


    def get_db_user(db_name):
        return secrets.db_connections[db_name]['user']
