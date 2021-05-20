from user.models import User


class SessionUserHandlingMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user_logged_in_session = None
        request.session_user = None

        if hasattr(request, "session") and "USER_LOGGED_IN_SESSION" in request.session.keys():
            user_logged_in_session = request.session["USER_LOGGED_IN_SESSION"]

        if user_logged_in_session:
            session_user = User.objects.filter(user_name=user_logged_in_session).first()
            request.session_user = session_user

        response = self.get_response(request)

        return response
