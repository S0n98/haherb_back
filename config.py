import os

class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or \
        'postgresql://postgres:Anhungu2010@localhost/haweb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ITEMS_PER_PAGE = 10
    SECRET_KEY = os.environ.get('SECRET_KEY') or '#1hardestkeyintheworld'
    AMBIGUOUS_NUMBERS = os.environ.get('AMBIGUOUS_NUMBERS') or [20, 22, 24]
    