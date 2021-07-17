import json.decoder
from datetime import datetime

from requests import Response
import random

class BaseCase:
    def get_answer(self, response: Response, name):
        try:
            response_as_dict = response.json()
        except json.decoder.JSONDecodeError:
            assert False, f"response is not JSON format. Response text is '{response.text}'"

        assert name in response_as_dict, f"Response not have '{name}'"

        return response_as_dict[name]

    def get_header(self, response: Response, headers_name):
        assert headers_name in response.headers, f"cannot find header"
        return response.headers[headers_name]
    
    def get_cookie(self, response: Response, cookie_name):
        assert cookie_name in response.cookies, f"cannot find cookie"
        return response.cookies[cookie_name]


    def prepare_register_data(self, email=None):
        if email is None:
            base_part = "ELITNIY"
            domain = "example.com"
            random_part = datetime.now().strftime("%m%d%Y%H%M%S")
            email = f"{base_part}{random_part}@{domain}"
        return {
            'password': '1234',
            'username': 'ELita',
            'firstName': 'ELita',
            'lastName': 'Elita',
            'email': email
        }

    def prepare_register_not_parametr(self, email=None):
        if email is None:
            base_part = "learnqa"
            domain = "example.com"
            random_part = datetime.now().strftime("%m%d%Y%H%M%S")
            email = f"{base_part}{random_part}@{domain}"
        return {
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': email
        }

    def prepare_register_one_symbol_nickname(self, email=None):
        if email is None:
            base_part = "learnqa"
            domain = "example.com"
            random_part = datetime.now().strftime("%m%d%Y%H%M%S")
            email = f"{base_part}{random_part}@{domain}"
        return {

            'password': '123',
            'username': 'l',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': email
        }

    def prepare_register_biglen_nickname(self, email=None):
        if email is None:
            base_part = "learnqa"
            domain = "example.com"
            random_part = datetime.now().strftime("%m%d%Y%H%M%S")
            email = f"{base_part}{random_part}@{domain}"
        return {

            'password': '123',
            'username': 'kiskikiskikiskikiskikiskikiskikiskikiskikiskikiskikiskikiskikiskikiskikiskikiskikiskikiskikiskikiskikiskikiskikiskikiskikiskikiskikiskikiskikiskikiskikiskikiskikiskikiskikiskikiskikiskikiskikiskikiskikiskikiskikiskikiskikiskikiskikiskikiskikiskikiskik',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': email
        }

    def prepare_register_first_user(self, email=None):
        if email is None:
            base_part = "firstus"
            random_part = random.randint(2, 1000)
            domain = "example.com"
            email = f"{base_part}{random_part}@{domain}"
        return {
            'password': '1234',
            'username': 'firstus',
            'firstName': 'firstus',
            'lastName': 'firstus',
            'email': email
        }

    def prepare_register_second_user(self, email=None):
        if email is None:
            base_part = "secondus"
            random_part = random.randint(2, 1000)
            domain = "example.com"
            email = f"{base_part}{random_part}@{domain}"
        return {
            'password': '1234',
            'username': 'secondus',
            'firstName': 'secondus',
            'lastName': 'secondus',
            'email': email
        }
