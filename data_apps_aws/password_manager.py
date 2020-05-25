import os
from data_apps_aws.paths import ProjectPaths

def get_passphrase_from_file(pphrase_file):

    # get passphrase from file
    f = open(pphrase_file, 'r')
    gpg_passphrase = f.read()

    # remove end of line characters
    if gpg_passphrase[-1:] == '\n':
        gpg_passphrase = gpg_passphrase[:-1]

    return gpg_passphrase


def gpg_credtls_fname(sub_path_name):
    
    return str(ProjectPaths.pass_manager_path) + '/' + sub_path_name


def decode_credtls(this_credtls_file, this_passphrase):

    credtls_query = subprocess.check_output(["gpg", "--pinentry-mode", "loopback", 
                                        "--passphrase", this_passphrase,
                                        "-d", this_credtls_file])

    decrypted_credtls = credtls_query.decode("utf-8")

    # remove end of line characters
    if decrypted_credtls[-1:] == '\n':
        decrypted_credtls = decrypted_credtls[:-1]
        
    return decrypted_credtls


def get_credtls(sub_path_name, this_passphrase):

    credtls_fname = gpg_credtls_fname(sub_path_name)

    return decode_credtls(credtls_fname, this_passphrase)


# get passphrase from environment variable
gpg_passphrase = os.getenv('GPG_PASSPHRASE', 'NOT_DEFINED')

# get passphrase from file
gpg_passphrase_fname = str(ProjectPaths.secret_path) + '/gpg_passphrase.txt'
gpg_passphrase = get_passphrase_from_file(gpg_passphrase_fname)

IS_DEPLOYED = os.getenv('IS_DEPLOYED', "False")

if IS_DEPLOYED == "True":

    db_connections = {

        'quandl': {'user': os.getenv('quandl_user', 'NOT_DEFINED'),
                   'api_token': os.getenv('quandl_api_token', 'NOT_DEFINED')
                   },

        'fred': {'api_token': os.getenv('fred_api_token', 'NOT_DEFINED')
                 },

        'slack_webhook': {'url': os.getenv('slack_webhook', 'NOT_DEFINED_YET')
                 },

        'slack_cyborg_app': {'api_token': os.getenv('slack_cyborg_app', 'NOT_DEFINED_YET')
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


else:

    db_connections = {

        'quandl': {'user': get_credtls('research/quandl/user.gpg', gpg_passphrase),
                   'api_token': get_credtls('research/quandl/api_token.gpg', gpg_passphrase)
                   },

        'fred': {'api_token': get_credtls('research/fred/api_token.gpg', gpg_passphrase)
                 },

        'slack_webhook': {'url': get_credtls('research/slack_webhook/url.gpg', gpg_passphrase)
                 },

        'slack_cyborg_app': {'api_token': get_credtls('research/slack_cyborg_app/api_token.gpg', gpg_passphrase)
                 },

        "econ_data": {"user": get_credtls('research/econ_data/user.gpg', gpg_passphrase),
                      "password": get_credtls('research/econ_data/password.gpg', gpg_passphrase),
                      "url": get_credtls('research/econ_data/url.gpg', gpg_passphrase),
                      },

        "econ_data_read": {"user": get_credtls('research/econ_data/user.gpg', gpg_passphrase),
                           "password": get_credtls('research/econ_data/password.gpg', gpg_passphrase),
                           "url": get_credtls('research/econ_data/url.gpg', gpg_passphrase),
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


if __name__=="__main__":

    get_db_user('econ_data')
