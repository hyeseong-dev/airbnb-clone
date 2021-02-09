from django.contrib import admin
from django.urls    import path,include
from users          import views


app_name = 'users'

urlpatterns = [
    path("login", views.LoginView.as_view(), name="login"),
    path("logout", views.log_out, name="logout"),
    path("signup", views.SignUpView.as_view(), name="signup"),
]

