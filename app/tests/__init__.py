import pytest


# enables pytest assert introspection in requests helpers
pytest.register_assert_rewrite("tests.utils_requests")
pytest.register_assert_rewrite("tests.utils_named_asserts")
