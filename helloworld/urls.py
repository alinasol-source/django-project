from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('delete/<city_name>/', views.delete_city, name='delete_city'),
    path('login', views.log_in, name="login"),
    path('logout', views.log_out, name="logout"),
    path('signup', views.sign_up, name="signup"),
]