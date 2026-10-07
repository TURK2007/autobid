from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),

    path("register/", views.register, name="register"),
    path("logout/", views.logout_view, name="logout"),

    path("create/", views.create_post, name="create_post"),
    path("post/<int:pk>/", views.detail, name="detail"),
    path("post/<int:pk>/edit/", views.edit_post, name="edit_post"),
    path("post/<int:pk>/delete/", views.delete_post, name="delete_post"),
    path("register/", views.register, name="register"),
    path("login/", views.user_login, name="login"),
    path("sell/", views.sell_car, name="sell_car"),
    path("logout/", views.user_logout, name="logout"),
    path('', views.home, name='index'),
    path('search/', views.search_view, name='search_view'),
]

