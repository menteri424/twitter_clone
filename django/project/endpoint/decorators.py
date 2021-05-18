import types
from user.models import User
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import View


def login_required(obj):
    """
    ログインしているかチェックし、未ログインだった場合indexページへ飛ばすデコレーター
    当然、Djangoの関数ベースViewやクラスベースViewで用いないとエラーが発生する
    """

    if type(obj) is types.FunctionType:
        # 関数ベースView
        def decorator(request, *args, **kwargs):
            redirect = _authentication(request)
            if redirect:
                return redirect
            return obj(request, *args, **kwargs)

        obj = decorator

        return obj  # function

    elif type(obj) is type:
        # クラスベースView
        dispatch = obj.dispatch

        def _dispatch(self, request, *args, **kwargs):
            redirect = _authentication(request)
            if redirect:
                return redirect
            return dispatch(self, request, *args, **kwargs)

        obj.dispatch = _dispatch

        return obj  # class


def _authentication(request):
    is_valid = False
    if "USER_LOGGED_IN_SESSION" in request.session.keys():
        user_name = request.session["USER_LOGGED_IN_SESSION"]
        is_valid = User.is_valid(user_name)
    if not is_valid:
        return redirect(reverse("login"))
