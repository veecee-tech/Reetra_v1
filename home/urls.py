from django.urls import path
from .views import Home, Privacy, contactUsView


urlpatterns = [
    path('', Home.as_view(), name="home" ),
    path('privacy-policy/', Privacy.as_view(), name="privacypolicy" ),
    path('contact/', contactUsView, name='contactus')
]
