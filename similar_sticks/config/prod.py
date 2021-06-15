from similar_sticks.config.base import BaseConfig


class ProductionConfig(BaseConfig):
    DATABASE_URI = 'sqlite:///:memory:'

    STICK_DATA_PATH = './stick_data.csv'
