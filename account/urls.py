from django.urls import path


from . import views

urlpatterns = [
    path("async-csrf/", views.get_async_csrf_token),
    path("api/account/login/", views.CustomAuthToken.as_view()),
    path("api/account/create/", views.ReplicaUserCreateAPIView.as_view()),
    path("api/account/signin/", views.SimpleLoginAPIView.as_view()),
]
