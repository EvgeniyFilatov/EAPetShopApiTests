import os
from dotenv import load_dotenv

# Загружаем переменные из файла .env
load_dotenv()

class Config:
    def __init__(self):
        # Читаем BASE_URL из .env
        self.BASE_URL = os.getenv('BASE_URL')
        if not self.BASE_URL:
            raise ValueError('BASE_URL не установлен в .env файле!')
        # Читаем TIMEOUT и преобразуем в число
        self.TIMEOUT = int(os.getenv('TIMEOUT', '10')) # таймаут для запросов
        # Уровень логирования
        self.LOG_LEVEL = os.getenv('LOG_LEVEL')

    def show_config(self):
        '''Показать текущую конфигурацию'''
        print(f'BASE_URL: {self.BASE_URL}')
        print(f'TIMEOUT: {self.TIMEOUT}')
        print(f'LOG_LEVEL: {self.LOG_LEVEL}')

# Создаем один объект конфигурации, который будем использовать везде
config = Config()