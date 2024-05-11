import allure
import pytest
import requests
import random
import json

BASE_URL = "https://demoqa.com/Account/v1"

list_of_letters_and_nums = [
    '1', '2', '3', '4', '5', 'b', 'Abf'
]

random_addition = random.choice(list_of_letters_and_nums)

example_user = {
    "userName": "testUserAPI9" + (5*random_addition),
    "password": "Testpassword0@"
}

print(example_user)
token = None
user_id = None

@allure.title("Тест создания пользователя")
def test_create_user():
    global user_id
    with allure.step("Создание пользователя"):
        response = requests.post(f"{BASE_URL}/User", json=example_user)
        assert response.status_code == 201, f"Не удалось создать пользователя: {response.status_code} {response.json()}"
        user_id = response.json().get("userID")

@allure.title("Тест генерации токена")
def test_generate_token():
    global token
    with allure.step("Генерация токена"):
        response = requests.post(f"{BASE_URL}/GenerateToken", json=example_user)
        assert response.status_code == 200, f"Не удалось сгенерировать токен: {response.status_code} {response.json()}"
        token = response.json().get("token")

@allure.title("Тест успешной авторизации")
def test_authorized_success():
    global token
    with allure.step("Авторизация пользователя"):
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.post(f"{BASE_URL}/Authorized", json=example_user, headers=headers)
        assert response.status_code == 200, f"Не удалось аутентифицировать пользователя: {response.status_code} {response.json()}"

@allure.title("Тест получения данных о пользователе")
def test_get_user_details():
    global token
    global user_id
    with allure.step("Отправка GET-запроса к конечной точке получения данных о пользователе"):
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get(f"{BASE_URL}/User/{user_id}", headers=headers)
        assert response.status_code == 200, f"Не удалось получить данные о пользователе: {response.status_code} {response.json()}"

@allure.title("Тест удаления пользователя")
def test_delete_user():
    global token
    global user_id
    with allure.step("Отправка DELETE-запроса к конечной точке удаления пользователя"):
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.delete(f"{BASE_URL}/User/{user_id}", headers=headers)
        if response.content:
            try:
                delete_message = response.json().get('message')
            except json.JSONDecodeError as e:
                allure.attach(response.content, 'Содержимое ответа')
                assert False, f"Не удалось декодировать содержимое ответа как JSON: {e}"
        else:
            delete_message = None
        assert delete_message != 'User Id not correct!', f"Сообщение об удалении 'User Id not correct!': {response.status_code} {response.content}"
        assert response.status_code == 200, f"Не удалось удалить пользователя: {response.status_code} {response.content}"
