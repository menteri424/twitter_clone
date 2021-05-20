from django.db import models
from django.db.models.fields.related import OneToOneField
from django.db.utils import IntegrityError


class User(models.Model):
    user_name = models.CharField("ユーザーID", max_length=20, unique=True)
    password = models.CharField("パスワード", max_length=20)
    full_name = models.CharField("名前", max_length=20)
    email = models.EmailField("メールアドレス", unique=True)
    profile = models.CharField("プロフィール", max_length=50, blank=True, null=True)
    url = models.URLField("URL", blank=True, null=True)
    birth_date = models.DateTimeField("誕生日", blank=True, null=True)
    followers = models.ManyToManyField("self", related_name="followes", symmetrical=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "user"

    @classmethod
    def is_valid_user_name(cls, user_name):
        # user_nameが利用可能かを調べる（現状存在確認だけ）
        return cls.objects.filter(user_name=user_name).exists()

    @classmethod
    def can_login(cls, user_name, password):
        return cls.objects.filter(user_name=user_name, password=password).exists()

    def try_follow(self, user):
        if self.is_following(user) or self == user:
            return False
        user.followers.add(self)
        return True

    def try_unfollow(self, user):
        if not self.is_following(user):
            return False
        user.followers.remove(self)
        return True

    def is_following(self, user):
        if user.followers.filter(id=self.id).exists():
            return True
        return False

