import sys

from data_apps_aws.src.paths import ProjectPaths

try:
    sys.path.append(str(ProjectPaths.secret_path))
    import passwords.secrets as sc

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
    return sc.db_connections[db_name]['api_token']


def get_db_url(db_name):
    return sc.db_connections[db_name]['url']


def get_db_password(db_name):
    return sc.db_connections[db_name]['password']


def get_db_user(db_name):
    return sc.db_connections[db_name]['user']
