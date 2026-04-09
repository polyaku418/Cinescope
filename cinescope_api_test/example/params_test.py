import pytest

@pytest.mark.parametrize("input_data,expected", [(1, 2), (2, 4), (3, 6)])
def test_multiply_by_two(input_data, expected):
    assert input_data * 2 == expected



@pytest.mark.parametrize("parameter_name", ["value1", "value2"])
class TestParametrizedClass:
    def test_first(self, parameter_name):
        print(f"Тест 1 прогон: {parameter_name}")
        assert True

    def test_second(self, parameter_name):
        print(f"Тест 2 прогон: {parameter_name}")
        assert True



@pytest.mark.parametrize("param_a,param_b", [
    ("a1", "b1"),
    ("a2", "b2")
])
class TestMultipleParams:

    def test_params_combination(self, param_a, param_b):
        print(f"1 тест: {param_a} и {param_b}")

    def test_another_method(self, param_a, param_b):
        combined = f"{param_a}-{param_b}"
        print(f"2 тест: {combined}")
        assert len(combined) > 2



@pytest.mark.parametrize("class_param", ["c1", "c2"])
class TestCombinedParametrization:
    @pytest.mark.parametrize("method_param", ["m1", "m2", "m3"])
    def test_combination(self, class_param, method_param):
        # Этот тест запустится 6 раз (2 параметра класса × 3 параметра метода)
        print(f"Тест 1 с параметризацией класса={class_param} и метода={method_param}")
        assert True

    def test_only_class_param(self, class_param):
        # Этот тест запустится 2 раза (только с параметрами класса)
        print(f"Тест 2 с параметризацией только класса={class_param}")
        assert True



@pytest.mark.parametrize("feature_flag,platform", [
    ("feature_a", "windows"),
    ("feature_a", "mac"),
    ("feature_b", "windows"),
    pytest.param("feature_b", "mac", marks=pytest.mark.skip(reason="Not supported on Mac"))
])
class TestFeatures:

    def test_feature_availability(self, feature_flag, platform):
        print(f"Testing {feature_flag} on {platform}")
        assert True



from cinescope_api_test.constants import SUPER_ADMIN

@pytest.mark.parametrize("email, password, expected_status", [
    (SUPER_ADMIN['email'], SUPER_ADMIN['password'], 200),  # Исправлено
    ("test_login1@email.com", "asdqwe123Q!", 401),
    ("", "password", 401),
], ids=["Admin login", "Invalid user", "Empty username"])
def test_login(email, password, expected_status, api_manager):
    login_data = {
        "email": email,
        "password": password
    }
    api_manager.auth_api.login_user(login_data=login_data, expected_status=expected_status)

