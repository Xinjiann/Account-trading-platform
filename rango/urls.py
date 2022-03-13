from django.urls import path
from rango import views

app_name = 'rango'
urlpatterns = [
    path('', views.index, name='index'),
    path('category/<slug:category_name_slug>/',
        views.show_category, name='show_category'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('account/<slug:account_name>/', views.account_detail, name='account_detail')
]