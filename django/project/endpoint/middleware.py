from user.models import User


class SessionUserHandlingMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if hasattr(request, "session"):
            user_loged_in_session = request.session["USER_LOGGED_IN_SESSION"]
            session_user = User.objects.filter(user_name=user_loged_in_session).first()
            request.session_user = session_user
        else:
            request.session_user = None

        response = self.get_response(request)

        return response
