from django.urls import path

from core import views

urlpatterns = [
    path('login', views.LoginView.as_view(), name="login"),
    path('profile', views.ProfileView.as_view(), name="profile"),
    path('signup', views.SingUpView.as_view(), name="signup"),
    path('update_password', views.UpdatePasswordView.as_view(), name="update_password"),
]