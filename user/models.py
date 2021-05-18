from django.db import models
from django.db.models.fields.related import OneToOneField


class User(models.Model):
    user_name = models.CharField("ユーザーID", max_length=20, unique=True)
    password = models.CharField("パスワード", max_length=20)
    full_name = models.CharField("名前", max_length=20)
    email = models.EmailField("メールアドレス", unique=True)
    profile = models.CharField("プロフィール", max_length=50, blank=True, null=True)
    url = models.URLField("URL", blank=True, null=True)
    birth_date = models.DateTimeField("誕生日", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "user"

    @classmethod
    def is_valid(cls, user_name):
        # IDが利用可能かを調べる（現状存在確認だけ）
        return cls.objects.filter(user_name=user_name).exists()

    @classmethod
    def can_login(cls, user_name, password):
        return cls.objects.filter(user_name=user_name, password=password).exists()


class UserFollowingRelation(models.Model):
    followees = models.ManyToManyField(User)
    follower = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="followed_by"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "follower"
