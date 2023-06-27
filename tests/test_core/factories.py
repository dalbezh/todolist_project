from factory import DictFactory, Faker, LazyAttribute
from faker import factory


class SignUpRequest(DictFactory):
    username = Faker('user_name')
    password = Faker('password')
    password_repeat = LazyAttribute(lambda o: o.password)


class LoginRequest(DictFactory):
    username = Faker('user_name')
    password = Faker('password')
