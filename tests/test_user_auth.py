from lib.my_requests import MyRequests
import pytest
from lib.assertions import Assertions
from lib.base_case import BaseCase

import allure

@allure.epic("AUTH case")
class TestUserAuth:
    exclude_params = [
        ("no_cookie"),
        ("no_token")
    ]

    def setup(self):
        data = {
            'email': 'vinkotov@example.com',
            'password':'1234'
        }
        response1 = MyRequests.post("/user/login", data=data)

        assert "auth_sid" in response1.cookies, "There is no auth cookie in the response"
        assert "x-csrf-token" in response1.headers, "There is no CSRF token header"
        assert "user_id" in response1.json(), "no user id in the response"

        self.auth_sid = response1.cookies.get("auth_sid")
        self.token = response1.headers.get("x-csrf-token")
        self.user_id_from_auth_method = response1.json()["user_id"]
    @allure.description("this test success auth user by email and password")
    def test_auth_user(self):
    
        response2 = MyRequests.get(
            "/user/auth",
            headers={"x-csrf-token":self.token},
            cookies={"auth_sid":self.auth_sid}
        )

        assert "user_id" in response2.json(), "there no user id in second response"
        user_id_in_check_method = response2.json()["user_id"]
        assert self.user_id_from_auth_method == user_id_in_check_method, "user id !="

    @allure.description("Test wrong auth")
    @pytest.mark.parametrize('condition', exclude_params)
    def test_negative__auth_check(self, condition):

        if condition == "no_cookie":
            response2 = MyRequests.get("/user/auth",
            headers= {"x-csrf-token":self.token} 
            )

        else:
            response2 = MyRequests.get("/user/auth",
            cookies={"auth_sid":self.auth_sid} 
            )

        assert "user_id" in response2.json(), "no user id in second response"
        #assert "user_id" in self.response2.json(), "no user id in second response"
        user_id_from_check_method = response2.json()["user_id"]

        assert user_id_from_check_method == 0, f"user {condition}"