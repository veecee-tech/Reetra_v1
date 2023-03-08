from django.urls import path
from . import views


app_name = 'authentication'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('profile/', views.user_profile_view, name="update-profile"),
    path('change-password/', views.change_password, name="change-password")
]
