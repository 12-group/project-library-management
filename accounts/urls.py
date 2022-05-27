from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
   path('', views.home,name='home'),
   path('search/', views.search_book,name='search'),
   path('search_result/', views.search_result_book,name='search_result'),
   path('detail_info/', views.detail_info_book,name='detail'),
   path('login/', views.loginPage,name='login'),
   path('register/', views.register,name='register'),
   path('logout/', views.logoutUser, name="logout"),
   path('reset_pass', views.home,name='reset_password'),
   path('account/', views.accountSettings, name="account"),
]