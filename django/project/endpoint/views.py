import endpoint.forms as forms
import endpoint.decorators as decorators
import django.views.generic as generic

from django.http import request, HttpResponseNotAllowed, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.db.models import Prefetch, Q
from user.models import User
from tweet.models import Tweet
from django.views.generic.list import ListView


def login(request):
    if request.method == "GET":
        form = forms.LoginForm()
        return render(request, "login.html", {"form": form})
    elif request.method == "POST":
        form = forms.LoginForm(request.POST)

        if not form.is_valid():
            # TODO エラー画面ができていないので後々作成する。
            return render(request, "login.html", {"type": "NG"})

        user_name = form.cleaned_data["user_name"]
        password = form.cleaned_data["password"]

        succeed = User.can_login(user_name=user_name, password=password)

        if not succeed:
            # TODO エラー画面ができていないので後々作成する。
            return render(request, "login.html", {"type": "NG"})

        request.session["USER_LOGGED_IN_SESSION"] = user_name

        return redirect(reverse("index"))


def logout(request):
    # セッションを消すだけでOK
    return render(request, "test.html")


@decorators.login_required
class IndexView(generic.TemplateView):
    template_name = "index.html"
    methods = ["GET"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # TODO: シンプルにsession_user_nameでいいかも。あとはmiddlewareでrequestにsession_userを設定するとよいかも。
        user_logged_in_session = self.request.session_user

        # followers = user_logged_in_session.followers.all()

        # tweets = Tweet.objects.filter(
        #     Q(user__in=followers) | Q(user__user_name=user_name_logged_in_session)
        # ).order_by("-id")

        # context["tweets"] = tweets
        context["session_user"] = user_logged_in_session

        return context

    def get(self, request, **kwargs):
        return super().get(request, **kwargs)


# TODO 入力が不正だった場合にエラーメッセージが現在表示されていない。
class RegisterView(generic.CreateView):
    model = User
    form_class = forms.RegisterForm
    template_name = "register.html"
    success_url = reverse_lazy("index")


@decorators.login_required
class TweetView(generic.View):
    def get(self, request, *args, **kwargs):
        return HttpResponseNotAllowed("ページの遷移が不正です。")

    def post(self, request, *args, **kwargs):
        # formがないため、空で投稿できてしまう
        user_name_logged_in_session = request.session["USER_LOGGED_IN_SESSION"]
        content = request.POST.get("content")
        user = User.objects.filter(user_name=user_name_logged_in_session).get()
        Tweet.objects.create(user=user, content=content)
        return redirect(reverse("index"))


class ProfileView(generic.base.ContextMixin, generic.View):
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        user_name_logged_in_session = self.request.session.get("USER_LOGGED_IN_SESSION")
        user_logged_in_session = User.objects.filter(user_name=user_name_logged_in_session).get()
        has_user_name_session = bool(user_name_logged_in_session)

        profile_user_name = kwargs["user_name"]
        profile_user = User.objects.filter(user_name=profile_user_name).get()
        
        tweets = Tweet.objects.filter(user=profile_user)

        # プロフィールのユーザーをフォローしているかどうか
        is_following = user_logged_in_session.is_following(profile_user)

        # セッションがない or セッションとプロフィールのユーザーが同じとき
        # TODO: disableはHTMLの属性にも存在してややこしいので修正する
        disable_follow_botton = (
            not has_user_name_session or user_logged_in_session == profile_user_name
        )

        context["is_following"] = is_following
        context["disable_follow_botton"] = disable_follow_botton
        context["profile_user"] = profile_user
        context["tweets"] = tweets

        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return render(request, "profile.html", context)


@decorators.login_required
class FollowingManageView(generic.View):
    def post(self, request, *args, **kwargs):
        if request.path == reverse("follow"):
            print("asd")
        elif request.path == reverse("unfollow"):
            print("aaaaaa")
        else:
            # あり得ない想定だが、念のため制御しておく
            return HttpResponseBadRequest("不正なリクエストです。")
