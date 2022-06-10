from django.urls import path

from . import views

urlpatterns = [
   path('', views.home,name='home'),
   path('search/', views.search_book,name='search'),
   path('search_result/', views.search_result_book,name='search_result'),
   path('detail_info/<str:pk>/', views.detail_info_book,name='detail'),
   path('cart/', views.cart,name='cart'),

   path('login/', views.loginPage,name='login'),
   path('register/', views.register,name='register'),
   path('logout/', views.logoutUser, name='logout'),
   path('password_change/', views.password_change,name='password_change'),
   path('password_change_done/', views.password_change_done,name='password_change_done'),
   path('account/', views.accountSettings, name='account'),

   
   path('librarian/', views.librarian_home, name="librarian"),
   path('borrowers/', views.borrowers, name="borrowers"),
   path('register_reader/', views.register_reader, name="register_reader"),
   path('request_onl/', views.request_onl, name="request_onl"),
   path('request_off/', views.request_off, name="request_off"),
   path('return_books/', views.return_book, name="return_books"),
   path('penalty_ticket/', views.penalty_ticket, name="penalty_ticket"),

   path('manager/manager_dashboard/', views.manager_dashboard, name="manager_dashboard"),
   path('manager/add_staff/', views.add_staff, name="add_staff"),


   path('list_book/', views.list_book, name="list_book"),
   path('thanh_ly/', views.thanh_ly, name="thanh_ly"),
   path('add_book/', views.add_book, name="add_book"),

   path('money_list/', views.money_list, name="money_list"),
]  