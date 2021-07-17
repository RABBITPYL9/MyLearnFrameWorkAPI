
from requests.models import Response
from lib import assertions
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


class TestUserRegister(BaseCase):
   
    def test_create_user_successfully(self):
        data = self.prepare_register_data()

        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 200)
        Assertions.json_has_key(response, "id")
    


    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_register_data(email)

        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", f"actual content {response.status_code}"

    def test_create_user_with_wrong_email(self):
        email = 'vinkotovexample.com'
        data = self.prepare_register_data(email)

        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Invalid email format"

    def test_create_user_not_one_parametr(self):
        data = self.prepare_register_not_parametr()
        
        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The following required params are missed: password"

    def test_create_user_short_nickname(self):
        data = self.prepare_register_one_symbol_nickname()
        response = MyRequests.post("/user/", data=data)
        
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The value of 'username' field is too short"

    def test_create_user_biglen_nickname(self):
        data = self.prepare_register_biglen_nickname()
        response = MyRequests.post("/user/", data=data)
        
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The value of 'username' field is too long"


