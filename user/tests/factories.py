import factory
import user.models as models


class UserFactory(factory.django.DjangoModelFactory):
    user_name = factory.Sequence(lambda n: "test{}".format(n))
    password = "123123"
    full_name = "テスト太郎"
    email = factory.Sequence(lambda n: "test{}@example.com".format(n))

    class Meta:
        model = models.User
