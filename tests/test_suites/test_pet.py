import allure
import jsonschema
import pytest
import random
from src.api.api_client import client
from tests.schemas.pet_schema import PET_SCHEMA


@allure.feature('Pet')
class TestPet:

        # ==== СОЗДАНИЕ ПИТОМЦЕВ ====

    @allure.title('Создание нового питомца (минимальные данные)')
    def test_create_pet_minimum_data(self):
        '''Тест на создание питомца с минимальным набором данных'''
        with allure.step('Подготовка данных'):

            pet_id = random.randint(1000, 9999)

            payload = {
                'id': pet_id,
                'name': 'Buddy',
                'status': 'available'
            }

        with allure.step('Отправка запроса на создание питомца'):
            response = client.post('/pet', payload)

        with allure.step('Проверка статуса ответа и валидация JSON-схемы'):
            assert response.status_code == 200, f'Код ответа не совпал с ожидаемым, код: {response.status_code}'

            response_data = response.json()
            jsonschema.validate(response_data, PET_SCHEMA)

            assert response_data['id'] == payload['id']
            assert response_data['name'] == payload['name']
            assert response_data['status'] == payload['status']

        # Очистка
        client.delete(f"/pet/{payload['id']}")

    @allure.title('Создание нового питомца (все поля)')
    def test_create_pet_full(self):
        '''Тест на создание питомца со всеми полями'''
        with allure.step('Подготовка данных'):

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

        with allure.step('Отправка зароса на создание питомца'):
            response = client.post('/pet', payload)

        with allure.step('Проверка статуса ответа и валидация JSON-схемы'):
            assert response.status_code == 200, f'Код ответа не совпал с ожидаемым, код: {response.status_code}'

            response_data = response.json()
            jsonschema.validate(response_data, PET_SCHEMA)

            assert response_data['id'] == payload['id']
            assert response_data['name'] == payload['name']
            assert response_data['category'] == payload['category']
            assert response_data['photoUrls'] == payload['photoUrls']
            assert response_data['tags'] == payload['tags']
            assert response_data['status'] == payload['status']

        # Очистка
        client.delete(f'/pet/{payload["id"]}')

        # ==== ПОЛУЧЕНИЕ ПОТОМЦЕВ ====

    @allure.title('Получение питомца по ID')
    def test_get_pet_by_id(self, create_pet):
        '''Тест получения информации о питомце по его ID'''
        pet_id = create_pet['id']

        with allure.step(f'Отправка запроса на получение информации о питомце по ID={pet_id}'):
            response = client.get(f'/pet/{pet_id}')

        with allure.step('Проверка статуса ответа и валидация JSON-схемы'):
            assert response.status_code == 200, f'Код ответа не совпал с ожидаемым, код: {response.status_code}'

            pet_data = response.json()
            jsonschema.validate(pet_data, PET_SCHEMA)

            assert pet_data['id'] == pet_id

    @allure.title('Поиск питомцев по статусу')
    @pytest.mark.parametrize('status', ['available', 'pending', 'sold'])
    def test_find_pets_by_status(self, status):
        '''Тест поиска питомцев по статусу'''
        with allure.step(f'Отправка запроса на поиск питомцев по статусу: {status}'):
            response = client.get(f'/pet/findByStatus', params={'status': status})

        with allure.step('Проверка статуса ответа'):
            assert response.status_code == 200, f'Код ответа не совпал с ожидаемым, код: {response.status_code}'

            pets = response.json()
            assert isinstance(pets, list)

            # Проверяем что все найденные питомцы имеют нужный статус
            for pet in pets:
                assert pet['status'] == status

        # ==== ОБНОВЛЕНИЕ ПИТОМЦЕВ =====

    @allure.title('Обновление питомца')
    def test_update_pet_put(self, create_pet_full):
        '''Тест полного обновления питомца через PUT'''
        pet_id = create_pet_full['id']

        with allure.step('Подготовка данных для обновления'):
            updated_data = {
                'id': pet_id,
                'name': 'Updated Doggie',
                'category': {
                    'id': 2,
                    'name': 'Updated Dogs'
                },
                'photoUrls': ['new_photo.jpg'],
                'tags': [
                    {
                        'id': 1,
                        'name': 'updated_tag'
                    }
                ],
                'status': 'sold'
            }

        with allure.step('Отправка запроса на обновление информации о питомце'):
            response = client.put('/pet', updated_data)

        with allure.step('Проверка статуса ответа и валидация JSON-схемы'):
            assert response.status_code == 200, f'Код ответа не совпал с ожидаемым, код: {response.status_code}'

            updated_pet = response.json()
            jsonschema.validate(updated_pet, PET_SCHEMA)

            assert updated_pet['name'] == updated_data['name']
            assert updated_pet['status'] == updated_data['status']

        # ===== УДАЛЕНИЕ ПИТОМЦЕВ =====

    @allure.title('Удаление питомца по ID')
    def test_delete_pet_by_id(self, create_pet):
        '''Тест на удаление питомца по ID'''
        pet_id = create_pet['id']

        with allure.step(f'Отправка запроса на удаление питомца с ID={pet_id}'):
            response = client.delete(f'/pet/{pet_id}')

        with allure.step('Проверка статуса ответа'):
            assert response.status_code == 200, f'Код ответа не совпал с ожидаемым, код: {response.status_code}'
            assert response.text == 'Pet deleted'

        with allure.step('Проверка, что питомец удален'):
            get_response = client.get(f'/pet/{pet_id}')
            assert get_response.status_code == 404, f'Код ответа не совпал с ожидаемым, код: {response.status_code}'

        # ===== НЕГАТИВНЫЕ ТЕСТЫ =====

    @allure.title('Получение информации о несуществующем питомце')
    def test_get_nonexistent_pet(self):
        '''Тест на получение информации о несуществующем питомце'''
        pet_id = random.randint(10000, 99999)

        with allure.step('Отправка запроса на получение информации о несуществующем питомце'):
            response = client.get(f'/pet/{pet_id}')

        with allure.step('Проверка статуса ответа'):
            assert response.status_code == 404, f'Код ответа не совпал с ожидаемым, код: {response.status_code}'
            assert 'not found' in response.text.lower()

    @allure.title('Удаление несуществующего питомца')
    def test_delete_nonexistent_pet(self):
        '''Тест на удаление несуществующего питомца'''
        pet_id = random.randint(10000, 99999)

        with allure.step('Отправка запроса на удаление несуществующего питомца'):
            response = client.delete(f'/pet/{pet_id}')

        with allure.step('Проверка статуса ответа'):
            assert response.status_code in [200, 404], f'Код ответа не совпал с ожидаемым, код: {response.status_code}'

    @allure.title('Обновление несуществующего питомца')
    def test_update_nonexistent_pet(self):
        '''Тест на удаление несуществующего питомца'''
        pet_id = random.randint(10000, 99999)

        with allure.step('Подготовка данных'):
            payload = {
                "id": pet_id,
                "name": "Non-existent Pet",
                "status": "available"
            }

        with allure.step('Отправка запроса на обновление несуществующего питомца'):
            response = client.put('/pet', payload)

        with allure.step('Проверка статуса ответа'):
            assert response.status_code == 404, f'Код ответа не совпал с ожидаемым, код: {response.status_code}'
            assert 'not found' in response.text.lower()

    @allure.title('Поиск питомцев по невалидному статусу')
    @pytest.mark.parametrize('invalid_status', ['invalid', 'wrong', '--', ''])
    def test_find_by_invalid_status(self, invalid_status):
        '''Тест на поиск питомцев по невалидному статусу'''
        with allure.step(f'поиск питомцев по невалидному статусу: {invalid_status}'):
            response = client.get('/pet/findByStatus', params={'status': invalid_status})

        with allure.step('Проверка статуса ответа'):
            assert response.status_code == 400, f'Код ответа не совпал с ожидаемым, код: {response.status_code}'

    # @allure.title('Создание питомца с невалидными данными')
    # @pytest.mark.parametrize('invalid_data', [
    #     {'id': '12345', 'name': 'test', 'status': 'available'},
    #     {'id': 1, 'name': 123, 'status': 'available'},
    #     {'id': 1, 'name': 123, 'status': 'invalid_status'}
    #     ])
    # def test_create_pet_invalid_data(self, invalid_data):
    #     '''Тест на создание питомца с невалидными данными'''
    #     with allure.step('Отправка запроса на создание питомца с невалидными данными'):
    #         response = client.post('/pet', invalid_data)
    #
    #     with allure.step('Проверка статуса ответа'):
    #         assert response.status_code == 400, f'Код ответа не совпал с ожидаемым, код: {response.status_code}'