from similar_sticks.config.base import BaseConfig


class LocalConfig(BaseConfig):
    TESTING = True
    DEBUG = True
    DATABASE_URI = 'sqlite:///:memory:'

    STICK_DATA_PATH = './stick_data.csv'
