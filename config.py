class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'\
                    .format(
                    user='nlclomzg',
                    pw='BIX18mbSMKRi2ZyEUm3cbg6Z5oc0Ail2',
                    url='rosie.db.elephantsql.com',
                    db='nlclomzg')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'\
                    .format(
                    user='nlclomzg',
                    pw='BIX18mbSMKRi2ZyEUm3cbg6Z5oc0Ail2',
                    url='rosie.db.elephantsql.com',
                    db='nlclomzg')
