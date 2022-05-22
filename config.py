
import os
# DATABASE_URL="postgresql://postgres:1234@127.0.0.1:5432/blogdb"
# 259f16ca1fb961b61def43711bbea85bb22cc0d2b3686f23a90314cbe36a145b
DATABASE_URL="postgresql://fqjcqskzzajktj:259f16ca1fb961b61def43711bbea85bb22cc0d2b3686f23a90314cbe36a145b@ec2-54-164-40-66.compute-1.amazonaws.com:5432/d29e479jc8pq4j"

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'
    SQLALCHEMY_DATABASE_URI = DATABASE_URL


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True