import pytest
import user.tests.factories as factories
import user.models as models


@pytest.mark.django_db
class TestUser:
    @pytest.mark.parametrize(
        "user_name, expected",
        [
            ("user1", True),
            ("user9", False),
        ],
    )
    def test_is_valid(self, user_name, expected):
        factories.UserFactory(user_name="user1")

        assert models.User.is_valid(user_name) == expected

    @pytest.mark.parametrize(
        "user_name, password, expected",
        [
            ("user1", "112233", True),
            ("user1", "111111", False),
            ("user9", "112233", False),
            ("user9", "111111", False),
        ],
    )
    def test_can_login(self, user_name, password, expected):
        factories.UserFactory(user_name="user1", password="112233")

        assert models.User.can_login(user_name, password) == expected
