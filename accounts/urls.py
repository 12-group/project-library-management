from django.urls import path
from . import views

urlpatterns = [
   path('', views.home,name='home'),
   path('search/', views.search_book,name='search'),
   path('search_result/', views.search_result_book,name='search_result'),
   path('detail_info/', views.detail_info_book,name='detail'),

]