import os
from data_apps_aws.paths import ProjectPaths
import subprocess

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


def getenv_save(this_env_var):
    return os.getenv(this_env_var, 'NOT_DEFINED')
    

IS_DEPLOYED = os.getenv('IS_DEPLOYED', "False")


if IS_DEPLOYED == "True":

    # get passphrase from environment variable
    gpg_passphrase = getenv_save('GPG_PASSPHRASE')

    db_connections = {

        'quandl': {'user': getenv_save('quandl_user'),
                   'api_token': getenv_save('quandl_api_token')
                   },

        'fred': {'api_token': getenv_save('fred_api_token')
                 },

        'slack_webhook': {'url': getenv_save('slack_webhook')
                 },

        'slack_cyborg_app': {'api_token': getenv_save('slack_cyborg_app')
                 },

        "econ_data": {"user": getenv_save('econ_data_user'),
                      "password": getenv_save('econ_data_password'),
                      "url": getenv_save('econ_data_url'),
                      },

        "econ_data_read": {"user": getenv_save('econ_data_read_user'),
                           "password": getenv_save('econ_data_read_password'),
                           "url": getenv_save('econ_data_read_url'),
                           },
    }


else:

    # get passphrase from file
    gpg_passphrase_fname = str(ProjectPaths.secret_path) + '/gpg_passphrase.txt'
    gpg_passphrase = get_passphrase_from_file(gpg_passphrase_fname)

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
