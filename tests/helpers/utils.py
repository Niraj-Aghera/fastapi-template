# Common test utilities and helper functions
import os
import random
import string
from contextlib import contextmanager
from pathlib import Path


def assert_raises(expected_exception, func, *args, **kwargs):
    """Assert that a function call raises the expected exception."""
    try:
        func(*args, **kwargs)
    except Exception as e:
        assert isinstance(e, expected_exception), f"Expected {expected_exception}, got {type(e)}"
    else:
        raise AssertionError(f"Expected exception {expected_exception} was not raised")


def assert_almost_equal(a, b, tol=1e-7):
    """Assert that two numbers are almost equal within a tolerance."""
    assert abs(a - b) <= tol, f"{a} != {b} within tolerance {tol}"


def random_string(length=8):
    """Generate a random string of given length."""
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))


def random_int(min_value=0, max_value=100):
    """Generate a random integer between min_value and max_value."""
    return random.randint(min_value, max_value)


@contextmanager
def patch_env(new_env):
    """Temporarily patch os.environ with new_env dict."""
    old_env = os.environ.copy()
    os.environ.update(new_env)
    try:
        yield
    finally:
        os.environ.clear()
        os.environ.update(old_env)


def load_test_data(file_path):
    """Load test data from a file."""
    with Path(file_path).open("r") as f:
        return f.read()
