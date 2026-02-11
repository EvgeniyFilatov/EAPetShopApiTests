import requests
import logging
from config import config

# Настраиваем логгер
logger = logging.getLogger(__name__)

class APIClient:

    def __init__(self):
        # Создаем сессию - она запоминает настройки между запросами
        self.session = requests.Session()
        # Настраиваем заголовки для ВСЕХ запросов
        # Теперь не нужно каждый раз указывать Content-Type
        self.session.headers.update({
            'Content_Type': 'application/json', # Мы отправляем JSON
            'Accept': 'application/json' # Мы принимаем JSON
        })
        # Базовый URL из конфига
        self.base_url = config.BASE_URL
        # Можно настроить прямо в сессии
        self.timeout = config.TIMEOUT

        logger.info(f'API клиент готов. База: {self.base_url}')

    # САМЫЕ ПРОСТЫЕ МЕТОДЫ
    def get(self, endpoint, **kwargs):
        '''GET запрос'''
        # Собираем URL прямо здесь
        clean_endpoint = endpoint.lstrip('/')
        url = f'{self.base_url}/{clean_endpoint}'
        logger.info(f'📨 GET {endpoint}')

        response = self.session.get(url, timeout=self.timeout, **kwargs)

        # Простая проверка статуса
        if response.status_code == 200:
            logger.info(f'✅ Успех: {response.status_code}')
        else:
            logger.warning(f'⚠️  Ошибка: {response.status_code}')

        return response

    def post(self, endpoint, json_data, **kwargs):
        '''POST запрос'''
        clean_endpoint = endpoint.lstrip('/')
        url = f'{self.base_url}/{clean_endpoint}'
        logger.info(f'📨 POST {endpoint}')

        response = self.session.post(url, json=json_data, timeout=self.timeout, **kwargs)

        if response.status_code == 200:
            logger.info(f'✅ Успех: {response.status_code}')
        else:
            logger.warning(f'⚠️  Ошибка: {response.status_code}')

        return response

    def put(self, endpoint, json_data, **kwargs):
        '''PUT запрос'''
        clean_endpoint = endpoint.lstrip('/')
        url = f'{self.base_url}/{clean_endpoint}'
        logger.info(f'📨 PUT {endpoint}')

        response = self.session.put(url, json=json_data, timeout=self.timeout, **kwargs)

        if response.status_code == 200:
            logger.info(f'✅ Успех: {response.status_code}')
        else:
            logger.warning(f'⚠️  Ошибка: {response.status_code}')

        return response

    def delete(self, endpoint, **kwargs):
        '''DELETE запрос'''
        clean_endpoint = endpoint.lstrip('/')
        url = f'{self.base_url}/{clean_endpoint}'
        logger.info(f'📨 DELETE {endpoint}')

        response = self.session.delete(url, timeout=self.timeout, **kwargs)

        if response.status_code == 200:
            logger.info(f'✅ Успех: {response.status_code}')
        else:
            logger.warning(f'⚠️  Ошибка: {response.status_code}')

        return response

client = APIClient()