import pytest
import random
import logging
import sys
from src.api.api_client import client

# 🌟 ВАЖНО: Настройка логирования для ВСЕХ тестов
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s | %(name)-25s | %(levelname)-8s | %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)  # Вывод в консоль
    ]
)

logger = logging.getLogger(__name__)

@pytest.fixture
def create_pet():
    '''Фикстура для создания питомца'''

    # Генерируем случайный ID, чтобы избежать конфликтов
    pet_id = random.randint(1000, 9999)

    payload = {
        'id': pet_id,
        'name': f'TestPet_{pet_id}',
        'status': 'available'
    }

    logger.info(f'Creating pet with ID: {pet_id}')

    # Создаем питомца (код ДО yield)
    response = client.post('/pet', payload)

    # Проверяем, что создание прошло успешно
    assert response.status_code == 200, f'Failed to create pet: {response.text}'

    # Получаем данные созданного питомца
    pet_data = response.json()

    # Возвращаем данные в тест
    yield pet_data

    # Очистка ПОСЛЕ теста (код ПОСЛЕ yield)
    logger.info(f'Cleaning up pet with ID: {pet_id}')

    try:
        # Пытаемся удалить питомца
        delete_response = client.delete(f'/pet/{pet_id}')

        if delete_response.status_code == 200:
            logger.info(f'Pet {pet_id} deleted successfully')
        else:
            logger.warning(f'Failed to delete pet {pet_id}: {delete_response.text}')
    except Exception as e:
        # Если удаление не удалось, просто логируем
        logger.error(f'Error during сleanup of pet {pet_id}: {str(e)}')

@pytest.fixture
def create_pet_full():
    '''Фикстура для создания питомца со всеми полями'''

    pet_id = random.randint(1000, 9999)

    payload = {
        'id': pet_id,
        'name': 'doggie',
        'category': {
            'id': 1,
            'name': 'Dogs'
        },
        'photoUrls': ['string'],
        'tags': [
            {
                'id': 0,
                'name': 'string'
            }
        ],
        'status': 'available'
    }

    response = client.post('/pet', payload)
    assert response.status_code == 200, f'Failed to create pet: {response.text}'

    pet_data = response.json()

    yield pet_data

    logger.info(f'Cleaning up pet with ID: {pet_id}')

    try:
        delete_response = client.delete(f'/pet/{pet_id}')

        if delete_response.status_code == 200:
            logger.info(f'Pet {pet_id} deleted successfully')
        else:
            logger.warning(f'Failed to delete pet {pet_id}: {delete_response.text}')
    except Exception as e:
        logger.error(f'Error during сleanup of pet {pet_id}: {str(e)}')


@pytest.fixture
def create_order(create_pet):
    '''Фикстура для создания заказа'''

    # Фикстура может использовать другие фикстуры
    # Здесь мы не создаем нового питомца, а используем существующего
    pet_id = create_pet['id'] # Используем реального питомца

    # Генерируем случайный ID для заказа
    order_id = random.randint(1000, 9999)

    # Данные для заказа
    payload = {
        'id': order_id,
        'petId': pet_id,
        'quantity': 1,
        'status': 'placed',
        'complete': True
    }

    logger.info(f'Creating order with ID: {order_id}')

    # Создаем заказ
    response = client.post('/store/order', payload)
    assert response.status_code == 200, f'Failed to create order: {response.text}'

    order_data = response.json()

    # Возвращаем данные в тест
    yield order_data

    # Очистка после теста
    logger.info(f'Cleaning up order with ID: {order_id}')

    try:
        delete_response = client.delete(f'/store/order/{order_id}')
        if delete_response.status_code == 200:
            logger.info(f'Order {order_id} deleted successfully')
    except Exception as e:
        logger.error(f'Error during cleanup of order {order_id}: {str(e)}')