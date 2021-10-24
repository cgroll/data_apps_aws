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


def get_service_credentials_cloud(db_name, credentials_type):


    if db_name == 'quandl':
        credentials_dict = {'user': getenv_save('quandl_user'),
                   'api_token': getenv_save('quandl_api_token')
                   },

    elif db_name == 'fred':
        credentials_dict = {'api_token': getenv_save('fred_api_token')
                 },

    elif db_name == 'rapidAPI':
        credentials_dict = {'api_token': getenv_save('rapid_api_token')
                 },

    elif db_name == 'slack_webhook':
        credentials_dict = {'url': getenv_save('slack_webhook')
                 },

    elif db_name == 'slack_cyborg_app':
        credentials_dict = {'api_token': getenv_save('slack_cyborg_app')
                 },

    elif db_name == "econ_data":
        credentials_dict = {"user": getenv_save('econ_data_user'),
                      "password": getenv_save('econ_data_password'),
                      "url": getenv_save('econ_data_url'),
                      },

    elif db_name == "econ_data_read":
        credentials_dict = {"user": getenv_save('econ_data_read_user'),
                           "password": getenv_save('econ_data_read_password'),
                           "url": getenv_save('econ_data_read_url'),
                           },

    elif db_name == "bfv_data":
        credentials_dict = {"user": getenv_save('bfv_data_user'),
                          "password": getenv_save('bfv_data_password'),
                          "url": getenv_save('bfv_data_url'),
                           }
    
    else:
        raise ValueError(f'Not credentials added for service {db_name} yet')

    return credentials_dict[credentials_type]


def get_service_credentials_local(db_name, credentials_type):

    # get passphrase from file
    try:
        gpg_passphrase_fname = str(ProjectPaths.secret_path) + '/gpg_passphrase.txt'
        gpg_passphrase = get_passphrase_from_file(gpg_passphrase_fname)
    except:
        raise ValueError(f'Reading passphrase from file did not work. Make sure that the path is correct: {gpg_passphrase_fname}')

    if db_name == 'quandl':

        credentials_dict = {'user': get_credtls('research/quandl/user.gpg', gpg_passphrase),
                   'api_token': get_credtls('research/quandl/api_token.gpg', gpg_passphrase)
                   }

    elif db_name == 'fred':

        credentials_dict = {'api_token': get_credtls('research/fred/api_token.gpg', gpg_passphrase)
                 }

    elif db_name == 'rapidAPI':

        credentials_dict = {'api_token': get_credtls('research/rapidAPI/api_token.gpg', gpg_passphrase)
                 }

    elif db_name == 'name_prism':
        credentials_dict = {'api_token': get_credtls('research/name_prism/api_token.gpg', gpg_passphrase)
                 }

    elif db_name == 'slack_webhook':
        credentials_dict = {'url': get_credtls('research/slack_webhook/url.gpg', gpg_passphrase)
                 }

    elif db_name == 'slack_cyborg_app':
        credentials_dict = {'api_token': get_credtls('research/slack_cyborg_app/api_token.gpg', gpg_passphrase)
                 }

    elif db_name == "econ_data":
        credentials_dict = {"user": get_credtls('research/econ_data/user.gpg', gpg_passphrase),
                      "password": get_credtls('research/econ_data/password.gpg', gpg_passphrase),
                      "url": get_credtls('research/econ_data/url.gpg', gpg_passphrase),
                      }
        
    elif db_name == "econ_data_read":
        credentials_dict = {"user": get_credtls('research/econ_data/user.gpg', gpg_passphrase),
                           "password": get_credtls('research/econ_data/password.gpg', gpg_passphrase),
                           "url": get_credtls('research/econ_data/url.gpg', gpg_passphrase),
                           }
        
    elif db_name == "bfv_data":
        credentials_dict = {"user": get_credtls('research/bfv_data/user.gpg', gpg_passphrase),
                     "password": get_credtls('research/bfv_data/password.gpg', gpg_passphrase),
                     "url": get_credtls('research/bfv_data/url.gpg', gpg_passphrase),
                      }
    elif db_name == 'openai':
        credentials_dict = {"api_token": get_credtls('research/open_ai/api_token.gpg', gpg_passphrase)}

    else:
        raise ValueError(f'Not credentials added for service {db_name} yet')

    return credentials_dict[credentials_type]


def get_service_credentials(db_name, credentials_type):

    if IS_DEPLOYED == "True":
        return get_service_credentials_cloud(db_name, credentials_type)
    else:
        return get_service_credentials_local(db_name, credentials_type)


def get_api_token(db_name):
    return get_service_credentials(db_name, 'api_token')


def get_db_url(db_name):
    return get_service_credentials(db_name, 'url')


def get_db_password(db_name):
    return get_service_credentials(db_name, 'password')


def get_db_user(db_name):
    return get_service_credentials(db_name, 'user')


if __name__=="__main__":

    get_db_user('econ_data')
