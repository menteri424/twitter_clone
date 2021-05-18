import endpoint.forms as forms
import endpoint.decorators as decorators
import django.views.generic as generic

from django.http import request, HttpResponseNotAllowed
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.db.models import Prefetch, Q
from user.models import User, UserFollowingRelation
from tweet.models import Tweet

def login(request):
    if request.method == "GET":
        form = forms.LoginForm()
        return render(request, "login.html", {"form": form})
    elif request.method == "POST":
        form = forms.LoginForm(request.POST)

        if not form.is_valid():
            return render(request, "login.html", {"type": "NG"})

        user_name = form.cleaned_data["user_name"]
        password = form.cleaned_data["password"]

        succeed = User.can_login(user_name=user_name, password=password)

        if not succeed:
            return render(request, "login.html", {"type": "NG"})

        request.session["USER_LOGGED_IN_SESSION"] = user_name

        return redirect(reverse("index"))


def logout(request):
    return render(request, "test.html")


@decorators.login_required
class IndexView(generic.TemplateView):
    template_name = "index.html"
    methods = ["GET"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_name = self.request.session["USER_LOGGED_IN_SESSION"]

        follower = UserFollowingRelation.objects.filter(followee__user_name=user_name).values_list(
            "followed_by"
        )
        tweets = Tweet.objects.filter(Q(user__in=follower) | Q(user__user_name=user_name))

        context["tweets"] = tweets
        context["user_name"] = user_name

        return context

    def get(self, request, **kwargs):
        return super().get(request, **kwargs)


class RegisterView(generic.CreateView):
    model = User
    form_class = forms.RegisterForm
    template_name = "register.html"
    success_url = reverse_lazy("index")


@decorators.login_required
class TweetView(generic.View):
    def get(self, request, **kwargs):
        return HttpResponseNotAllowed("ページの遷移が不正です。")

    def post(self, request, **kwargs):
        user_name = request.session["USER_LOGGED_IN_SESSION"]
        content = request.POST.get("content")
        user = User.objects.filter(user_name=user_name).get()
        Tweet.objects.create(user=user, content=content)
        return redirect(reverse("index"))

#TODO 他人のプロフィール表示,セッションの有無でフォローボタンを押したときにloginさせる
