from requests.models import Response
from lib.my_requests import MyRequests
import requests
from lib import assertions
from lib.base_case import BaseCase
from lib.assertions import Assertions
import json


class TestUserDelete(BaseCase):
    def test_delete_user(self):
        #login test user


        login_data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")
        user_id = Assertions.assert_json_value_by_name(response2, "user_id", 2, "error login")

        #try delete user with id 2

        response3 = MyRequests.delete("/user/2",
            headers = {"x-csrf-token": token},
            cookies = {"auth_sid": auth_sid}
            )

        #проверяем что пользователя с ид 2 не удалили
        assert response3.content.decode("utf-8") == f"Please, do not delete test users with ID 1, 2, 3, 4 or 5."

        #второй запрос для запроса юзера по ид

        #response4 = requests.get("https://playground.learnqa.ru/api/user/2")
        response4 = MyRequests.get("/user/2")

        Assertions.assert_json_value_by_name(response4, "username", "Vitaliy", "user delete with id 2")

    def test_positive_delete_user(self):
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
        get_user_id = self.get_answer(response2, "user_id")


        # delete new user test
        # response3 = requests.delete(f"https://playground.learnqa.ru/api/user/{get_user_id}", data=login_data,
        #                               headers={"x-csrf-token": token},
        #                               cookies={"auth_sid": auth_sid}
        #                               )

        response3 = MyRequests.delete(f"/user/{get_user_id}", data=login_data,
                                      headers={"x-csrf-token": token},
                                      cookies={"auth_sid": auth_sid}
                                      )


        response4 = MyRequests.get(f"/user/{get_user_id}")



        assert response4.content.decode("utf-8") == f"User not found"
