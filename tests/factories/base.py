from factory import Factory
from faker import Faker


# Shared faker instance
fake = Faker()


class BaseFactory(Factory):
    """Base factory with common config for all factories."""

    class Meta:
        abstract = True  # prevents direct use

    # Example: if all models share a timestamp, you could define it here
