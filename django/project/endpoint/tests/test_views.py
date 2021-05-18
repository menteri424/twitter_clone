import pytest
import user.tests.factories as factories
import user.models as models

from django.urls import reverse
from django.test import Client
from unittest.mock import patch


@pytest.mark.django_db
class TestLogin:
    def test_it(self, web_app):
        factories.UserFactory(user_name="user1", password="123123")

        res = web_app.get(reverse("login"))

        form = res.form
        form["user_name"] = "user1"
        form["password"] = "123123"

        res = form.submit()

        # リダイレクトしていること
        assert res.status_code == 302

        # リダイレクト先がindexページであること
        assert res.url == reverse("index")

        # セッションが作成されていること
        assert res.client.session["USER_LOGGED_IN_SESSION"] == "user1"

    def test_get(self, web_app):
        res = web_app.get(reverse("login"))
        assert res.status_code == 200

    def test_is_not_valid(self, web_app):
        with patch("endpoint.forms.LoginForm.is_valid", return_value=False):
            res = web_app.post(reverse("login"))

        # ログインページに戻っていること
        assert res.status_code == 200

    def test_is_valid_but_not_exists(self, web_app):
        with patch("endpoint.forms.LoginForm") as mock_form:
            mock_form.is_valid.return_value = True
            mock_form.cleaned_data = {"user_name": "test", "password": "123123"}

            with patch("user.models.User.can_login", return_value=False):
                res = web_app.post(reverse("login"))

        # ログインページに戻っていること
        assert res.status_code == 200


@pytest.mark.django_db
class TestIndex:
    def test_without_login(self, web_app):
        res = web_app.get(reverse("index"))

        # ログインページへリダイレクトすること
        assert res.status_code == 302
        assert res.url == reverse("login")
