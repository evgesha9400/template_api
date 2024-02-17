import pytest


@pytest.fixture
def dict_to_query_param():
    def convert(params_dict):
        query_params_list = []
        for key, value in params_dict.items():
            if isinstance(value, list):
                for item in value:
                    query_params_list.append((key, item))
            else:
                query_params_list.append((key, value))
        return query_params_list
    return convert
