import factory
import tweet.models as models
from user.tests.factories import UserFactory

class TweetFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    content = "123"

    class Meta:
        model = models.Tweet
