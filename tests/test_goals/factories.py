import factory


class CreateGoalCategoryRequest(factory.DictFactory):
    title = factory.Faker('catch_phrase')


class CreateGoalRequest(factory.DictFactory):
    title = factory.Faker('catch_phrase')
