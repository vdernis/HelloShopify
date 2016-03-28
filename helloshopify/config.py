import os

class DefaultConfig(object):

    PROJECT = "Hello Shopify"
    PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

    DEBUG = True
    TESTING = False

    SECRET_KEY = 'secret key'

    SERVER_NAME = "localhost:5000"
    PREFERRED_URL_SCHEME = "https"

    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/helloshopify.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_ECHO = True

    SHOPIFY_API_KEY = 'YOUR API KEY'
    SHOPIFY_SHARED_SECRET = 'YOUR SHARED SECRET'