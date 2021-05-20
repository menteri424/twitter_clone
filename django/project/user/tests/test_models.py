import pytest
import user.tests.factories as factories
import user.models as models

from unittest.mock import patch
from django.db.utils import IntegrityError


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

        assert models.User.is_valid_user_name(user_name) == expected

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
    
    @pytest.mark.parametrize("already_exsists", [True, False])
    def test_try_follow(self, already_exsists):
        followee = factories.UserFactory(user_name="followee")
        follower = factories.UserFactory(user_name="follower")

        if already_exsists:
            # 既にフォローしている場合
            assert follower.try_follow(followee)
            assert not follower.try_follow(followee)
        else:
            # フォローしていない場合
            assert follower.try_follow(followee)
            assert followee.followers.filter(id=follower.id).exists()

    @pytest.mark.parametrize("already_exsists", [True, False])
    def test_try_unfollow(self, already_exsists):
        followee = factories.UserFactory(user_name="followee")
        follower = factories.UserFactory(user_name="follower")

        if already_exsists:
            # 既にフォローしている場合
            followee.followers.add(follower) # followerがfolloweeをフォローする
            assert follower.try_unfollow(followee)
            assert not followee.followers.filter(id=follower.id).exists()
        else:
            # フォローしていない場合
            assert not follower.try_unfollow(followee)
