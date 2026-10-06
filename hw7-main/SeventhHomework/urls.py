from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [path('login/', auth_views.LoginView.as_view(template_name='library/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('books/', views.book_list_view, name='book_list'),
    path('readers/', views.reader_list_view, name='reader_list'),
    path('readers/<int:pk>/', views.reader_detail_view, name='reader_detail'),
]