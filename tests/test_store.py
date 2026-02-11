import random
import allure
import jsonschema
import pytest
from api_client import client
from tests.schemas.store_schema import STORE_SCHEMA, INVENTORY_SCHEMA


@allure.feature('Store')
class TestStore:

    #  ==== ИНВЕНТРАЬ ====

    @allure.title('Получение инвентаря магазина')
    def test_get_inventory(self):
        '''Тест на получение инвентаря магазина'''
        with allure.step('Отправка запроса на получение инвентаря магазина'):
            response = client.get('/store/inventory')

        with allure.step('Проверка статуса ответа и валидция JSON-схемы'):
            assert response.status_code == 200, f'Код ответа не совпал с ожидаемым, код: {response.status_code}'

            inventory_data = response.json()
            jsonschema.validate(inventory_data, INVENTORY_SCHEMA)

            # Проверяем что есть хотя бы одно поле
            assert len(inventory_data) > 0

    # ==== РАБОТА С ЗАКАЗАМИ ====

    @allure.title('Создание нового заказа')
    def test_create_order(self):
        '''Тест на создание нового заказа'''
        with allure.step('Подготовка данных зааказ'):
            order_id = random.randint(1000, 9999)

            payload = {
                'id': order_id,
                'petId': 1,
                'quantity': 7,
                'status': 'approved',
                'complete': True
            }

        with allure.step('Отправка запроса на создание нового заказа'):
            response = client.post('/store/order', payload)

        with allure.step('Проверка статуса ответа и валидация JSON-схемы'):
            assert response.status_code == 200, f'Код ответа не совпал с ожидаемым, код: {response.status_code}'

            order_data = response.json()
            jsonschema.validate(order_data, STORE_SCHEMA)

            assert order_data['id'] == payload['id']
            assert order_data['petId'] == payload['petId']
            assert order_data['quantity'] == payload['quantity']
            assert order_data['status'] == payload['status']
            assert order_data['complete'] == payload['complete']

        # Очистка
        client.delete(f'/store/order/{payload['id']}')

    @allure.title('Получение заказа по ID')
    def test_get_order_by_id(self, create_order):
        '''Тест на полчение заказа по его ID'''
        order_id = create_order['id']

        with allure.step(f'Отправка запроса на получение заказа по ID={order_id}'):
            response = client.get(f'/store/order/{order_id}')

        with allure.step('Проверка статуса ответа и валидация JSON-схемы'):
            assert response.status_code == 200, f'Код ответа не совпал с ожидаемым, код: {response.status_code}'

            order_data = response.json()
            jsonschema.validate(order_data, STORE_SCHEMA)

            assert order_data['id'] == order_id
            assert order_data['petId'] == create_order['petId']
            assert order_data['quantity'] == create_order['quantity']
            assert order_data['status'] == create_order['status']
            assert order_data['complete'] == create_order['complete']

    @allure.title('Удаление заказа по ID')
    def test_delete_order_by_id(self, create_order):
        '''Тест на удаление заказа по его ID'''
        order_id = create_order['id']

        with allure.step('Отправка запроса на удаление заказа по его ID'):
            response = client.delete(f'/store/order/{order_id}')

        with allure.step('Проверка статуса ответа'):
            assert response.status_code == 200, f'Код ответа не совпал с ожидаемым, код: {response.status_code}'

        with allure.step('Проверка, что заказ удален'):
            get_response = client.get(f'/store/order/{order_id}')

        with allure.step('Проверка статуса ответа'):
            assert get_response.status_code == 404, f'Код ответа не совпал с ожидаемым, код: {response.status_code}'

    # ===== НЕГАТИВНЫЕ ТЕСТЫ =====

    @allure.title('Получение несуществующего заказа')
    def test_get_nonexistent_order(self):
        '''Тест на получение несуществующего заказа'''
        order_id = random.randint(10000, 99999)

        with allure.step('Отправка запроса на получение несуществующего заказа'):
            response = client.get(f'/store/order/{order_id}')

        with allure.step('Проверка статуса ответа'):
            assert response.status_code == 404, f'Код ответа не совпал с ожидаемым, код: {response.status_code}'
            assert 'not found' in response.text.lower()

    @allure.title('Удаление несуществующего заказа')
    def test_delete_nonexistent_order(self):
        '''Тест на удаление несуществующего заказа'''
        order_id = random.randint(10000, 99999)

        with allure.step('Отправка запроса на удаление несуществующего заказа'):
            response = client.delete(f'/store/order/{order_id}')

        with allure.step('Проверка статуса ответа'):
            assert response.status_code == 200, f'Код ответа не совпал с ожидаемым, код: {response.status_code}'

    # @allure.title('Создание заказа с невалидными данными')
    # @pytest.mark.parametrize('invalid_data', [
    #     {'id': '123', 'petId': 1, 'quantity': 1, 'status': 'approved', 'complete': True},  ## id не число
    #     {'id': 1, 'petId': '1', 'quantity': 1, 'status': 'approved', 'complete': True},  ## petId не число
    #     {'id': 1, 'petId': 1, 'quantity': 1, 'status': 'invalid_status', 'complete': True},  ## невалидный статус
    #     {'id': 1, 'petId': 1, 'quantity': -1, 'status': 'approved', 'complete': True},  ## отрицательное количество
    #     {'id': 1, 'petId': 1, 'quantity': 1, 'status': 'approved', 'complete': 'True'}, ## True как строка
    # ])
    # def test_create_order_invalid_data(self, invalid_data):
    #     '''Тест на создание заказа с невалидными данными'''
    #     with allure.step('Отправка запроса на создание заказа с невалидными данными'):
    #         response = client.post('/store/order', invalid_data)
    #
    #     with allure.step('Проверка статуса ответа'):
    #         assert response.status_code == 400