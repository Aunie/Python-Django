from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("products/", views.products, name="products"),
    path("customers/<str:pk_test>/", views.customer, name="customers"),
    path("create_order/<str:pk>", views.createOrder, name="create_order"),
    path("update_order/<str:pk>", views.UpdateOrder, name="update_order"),
    path("delete_order/<str:pk>", views.deleteOrder, name="delete_order"),
    path("login", views.login_page, name="login"),
    path("logout", views.logout_user, name="logout"),
    path("register", views.register_page, name="register"),

]
