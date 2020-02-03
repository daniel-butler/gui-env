import os
from pathlib import Path
import urllib.parse

import pyodbc
from dotenv import load_dotenv, find_dotenv

load_dotenv()

default_mssql_driver = None
for available_driver in pyodbc.drivers():
    if available_driver.find('SQL SERVER'):
        default_mssql_driver = available_driver


def get_project_root() -> Path:
    return Path(os.path.dirname(os.path.abspath(__file__)))


PROJECT_ROOT = get_project_root()


# Validation of configs
def is_valid():
    for validator in VALIDATORS:  # Validators found at bottom of file
        validator()


def validate_able_to_find_dotenv_file():
    if find_dotenv() == '':
        raise NotConfiguredCorrectlyError(
            f'No .env file found. Refer to Readme.md for proper configuration. '
            f'Locations looked at started here {__file__}'
        )


# Settings that effect behavior
def get_authorization_usage_status() -> bool:
    use_auth = os.getenv('USE_AUTH', True)
    if use_auth in ['False', 'false', '0']:
        return False
    return bool(use_auth)


def get_testing_status() -> bool:
    testing = os.getenv('CI', False)
    if testing is False:
        return False
    if testing.lower() in ['false', '0']:
        return False
    return bool(testing)


# Settings that effect locations
def get_mssql_uri() -> str:
    user = os.getenv('MSSQL_USER', None)
    password = os.getenv('MSSQL_PASSWORD', None)
    server = os.getenv('MSSQL_SERVER', 'production')
    database = os.getenv('MSSQL_DATABASE', 'custom')
    driver = urllib.parse.quote_plus(os.getenv('MSSQL_DRIVER', default_mssql_driver))
    return f'mssql+pyodbc://{user}:{password}@{server}/{database}?driver={driver}'


def validate_mssql_uri() -> None:
    database_uri = get_mssql_uri().lower()
    if r'mssql+pyodbc://none:none' in database_uri:
        raise NotConfiguredCorrectlyError(f'MSSQL url .env variables not set correctly please refer to Readme.md')
    if 'production' in database_uri and get_testing_status():
        raise NotConfiguredCorrectlyError(
            'Set Database to something other than production. Tests remove all data in the database'
        )


def get_logging_folder() -> Path:
    logging_folder = os.getenv('LOGGING_FOLDER', PROJECT_ROOT)
    return Path(logging_folder)


def get_load_file_save_location() -> Path:
    save_location = os.getenv('BATCH_LOAD_FILE_SAVE_LOCATION', PROJECT_ROOT)
    return Path(save_location)


def get_connect_remittance_hot_folder() -> Path:
    hot_folder = os.getenv('CONNECT_REMITTANCE_HOT_FOLDER', PROJECT_ROOT)
    return Path(hot_folder)


def get_email_host_and_port() -> dict:
    host = os.getenv('EMAIL_HOST', 'mailhog')
    port = 1025 if host in ('mailhog', '127.0.0.1') else 25
    http_port = 8025
    return {'host': host, 'port': port, 'http_port': http_port}


def get_import_je_save_location() -> Path:
    save_location = os.getenv('IMPORT_JE_SAVE_LOCATION', PROJECT_ROOT)
    return Path(save_location)


# HTTP Settings
def get_flask_secret_key():
    secret_key = os.getenv('FLASK_SECRET_KEY', b'\x91\x909\x1aO\x12a\xd6N\x14(\x9c\x93[6E')
    return secret_key


def validate_flask_secret_key():
    testing = get_testing_status()
    secret_key = get_flask_secret_key()
    unsecure_flask_key = b'\x95\x907\x1aO\x12a\xd6N\x14(\x9c\x93[6E'
    if not testing and secret_key == unsecure_flask_key:
        raise NotConfiguredCorrectlyError(f'Set a secure flask key when in production. Please refer to Readme.md')
        

def get_url_prefix():
    prefix = os.getenv('URL_PREFIX', '/')
    if prefix[0] != '/':
        prefix = '/' + prefix
    if prefix[-1] != '/':
        prefix = prefix + '/'
    return prefix


def get_url_root():
    url_root = os.getenv('URL_ROOT', 'http://127.0.0.1')
    if url_root[-1] == '/':
        return url_root[:-1]
    return url_root


def validate_url_root():
    url_root = get_url_root()
    http_part = url_root[:8]
    if 'https://' not in http_part and 'http://' not in http_part:
        raise NotConfiguredCorrectlyError(
            f'The URL root should include either http:// or https:// at the beginning. Current value is {url_root}'
        )
    testing = get_testing_status()
    if not testing and ('127.0.0.1' in url_root or '0.0.0.0' in url_root):
        raise NotConfiguredCorrectlyError(f'Url root must be specified in production. Current value is {url_root}')


VALIDATORS = [
    validate_able_to_find_dotenv_file,
    validate_mssql_uri,
    validate_flask_secret_key,
    validate_url_root,
]


class NotConfiguredCorrectlyError(ValueError):
    pass
