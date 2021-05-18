from django import forms
from user.models import User
from tweet.models import Tweet


class LoginForm(forms.Form):
    user_name = forms.CharField(label="ユーザーID", max_length=20, required=True)
    password = forms.CharField(label="パスワード", max_length=20, required=True)


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            "user_name",
            "password",
            "full_name",
            "email",
            "profile",
            "url",
            "birth_date",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({"placeholder": field.label})


class Tweet(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ("user", "content")
