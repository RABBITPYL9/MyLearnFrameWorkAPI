from requests.models import Response
from lib.my_requests import MyRequests
import requests
from lib import assertions
from lib.base_case import BaseCase
from lib.assertions import Assertions


class TestUserEdit(BaseCase):
    def test_edit_just_created_user(self):
        # REGISTER
        register_data = self.prepare_register_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.json_has_key(response1, "id")

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_answer(response1, "id")

        # LOGIN

        login_data = {
            'email': email,
            'password': password
        }

        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")


        # EDIT

        new_name = "Changed"

        response3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_name})


        Assertions.assert_code_status(response3, 200)

        # GET

        response4 = MyRequests.get(f"/user/{user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid})

        Assertions.assert_json_value_by_name(
            response4,
            "firstName",
            new_name,
            "Wrong name"
        )

        # EDIT HOMEWORK 1
        #- Попытаемся изменить данные пользователя, будучи неавторизованными
    def test_try_edit_user_not_auth(self):
        new_name1 = "ChangedFIXIK"

        response9 = MyRequests.put(
            f"/user/3619",
            data={"firstName": new_name1})


        Assertions.assert_code_status(response9, 400)
        assert response9.content.decode("utf-8") == f"Auth token not supplied"
        #- Попытаемся изменить данные пользователя, будучи авторизованными другим пользователем
    def test_try_edit_another_user(self):
        # REGISTER with first user
        register_data = self.prepare_register_first_user()
        response1 = MyRequests.post("/user/", data=register_data)

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_answer(response1, "id")
        #save reg data
        saved_email_first = email

        # LOGIN with first user

        login_data = {
            'email': saved_email_first,
            'password': password
        }

        response2 = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")


          # REGISTER with 2 user
        register_data1 = self.prepare_register_second_user()
        response5 = MyRequests.post("/user/", data=register_data1)


        email1 = register_data1['email']
        first_name1 = register_data1['firstName']
        password1 = register_data1['password']
        user_id1 = self.get_answer(response5, "id")
        #save reg data
        saved_email_second = email1
        # LOGIN with 2user

        login_data1 = {
            'email': saved_email_second,
            'password': password1
        }

        response4 = MyRequests.post("/user/login", data=login_data1)
        auth_sid2 = self.get_cookie(response4, "auth_sid")
        token2 = self.get_header(response4, "x-csrf-token")


        # EDIT меняем данные, авторизуясь по кукам первого юзера, изменяя имя у первого

        new_name = "Changed"

        response3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token2},
            cookies={"auth_sid": auth_sid2},
            data={"firstName": new_name})

        Assertions.assert_code_status(response3, 200)

        # GET

        response4 = MyRequests.get(f"/user/{user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid})

        #проверяем что у второго пользователя осталось имя как и при регистрации
        Assertions.assert_json_value_by_name(
            response4,
            "firstName",
            'firstus',
            "Wrong name"
        )
        #- Попытаемся изменить email пользователя, будучи авторизованными тем же пользователем, на новый email без символа @
    def test_change_email_not_symbol_dog(self):
        # REGISTER user for test change email symbol
        register_data = self.prepare_register_first_user()
        response1 = MyRequests.post("/user/", data=register_data)

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_answer(response1, "id")
        # save reg data
        saved_email = email

        # LOGIN

        login_data = {
            'email': saved_email,
            'password': password
        }

        response2 = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")


        #change email

        new_email = "intellectmail.ru"

        response3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"email": new_email})


        # GET

        response4 = MyRequests.get(f"/user/{user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid})

        # проверяем что у второго пользователя осталось имя как и при регистрации
        Assertions.assert_json_value_by_name(
            response4,
            "email",
            f'{saved_email}', #почта как при регистрации
            "Wrong email"
        )
        #- Попытаемся изменить firstName пользователя, будучи авторизованными тем же пользователем, на очень короткое значение в один символ
    def test_change_firstname_minlen(self):
        # REGISTER user for test change first name is 1 symbol
        register_data = self.prepare_register_first_user()
        response1 = MyRequests.post("/user/", data=register_data)

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_answer(response1, "id")
        # save reg data
        saved_email = email
        assert_name = "firstus"

        # LOGIN

        login_data = {
            'email': saved_email,
            'password': password
        }

        response2 = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")


        #change FirstName

        new_name = "A"

        response3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_name})

        # GET

        response4 = MyRequests.get(f"/user/{user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid})

        # проверяем что у второго пользователя осталось имя как и при регистрации
        Assertions.assert_json_value_by_name(
            response4,
            "firstName",
            f'{first_name}',
            "Wrong name"
        )