

from django.urls import path, re_path
from . import views



urlpatterns = [
    path('', views.base),
    path('list_of_persons/', views.MainView.as_view()),
    path('info_persons/', views.List.as_view()),
    re_path(r'info_persons/(?P<param>\w*)/', views.List.as_view()),
    path('register/', views.RegisterFormView.as_view()),
    path('login/', views.LoginFormView.as_view()),
    path('logout/', views.LogoutView.as_view()),


]
