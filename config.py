import os

class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ITEMS_PER_PAGE = 10
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    
