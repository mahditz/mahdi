from django.urls import path
from . import views

app_name = 'watches'

urlpatterns = [
    path('', views.home, name='home'),
    path('watches/', views.watch_list, name='watch_list'),
    path('watches/<slug:slug>/', views.watch_detail, name='watch_detail'),

    path('category/', views.category_list, name='category'),  # لیست همه دسته‌ها
    path('category/<slug:slug>/', views.category_detail, name='category'),  # اینجا تغییر داده شده

    path('contact/', views.contact, name='contact'),
]
