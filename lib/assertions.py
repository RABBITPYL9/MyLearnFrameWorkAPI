from requests import Response, status_codes
import json

class Assertions:
    @staticmethod
    def assert_json_value_by_name(response: Response, name, expected_value, error_message):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not JSON format. Response text is '{response.text}'"

        assert name in response_as_dict, f"rsponse JSON not have key '{name}'"
        assert response_as_dict[name] == expected_value, error_message

    @staticmethod
    def json_has_key(response: Response, name):
         
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not JSON format. Response text is '{response.text}'"

        assert name in response_as_dict, f"rsponse JSON not have key '{name}'"

    @staticmethod
    def assert_code_status(response: Response, expected_code):
        assert response.status_code == expected_code, \
            f"error! expectet: {expected_code} . Actual: {response.status_code}"

    @staticmethod
    def json_has_no_key(response: Response, name):
         
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not JSON format. Response text is '{response.text}'"

        assert name not in response_as_dict, f"rsponse JSON  key '{name}' is not present"
    
    @staticmethod
    def json_has_keys(response: Response, names: list):
         
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not JSON format. Response text is '{response.text}'"
        
        for name in names:
            assert name in response_as_dict, f"rsponse JSON not have key '{name}'"
