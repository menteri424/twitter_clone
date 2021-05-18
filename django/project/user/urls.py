from django.urls import path


app_name = "user"
urlpatterns = [path("", index_view, name="index")]
