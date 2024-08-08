from django.urls import path
from . import views

# app_name = "accounts"

urlpatterns = [
    path("", views.home, name="home"),
    # path("test", views.IndexView.as_view(), name="test"),
    # path("testListView", views.IndexListView.as_view(), name="testListView"),
    # path("customer_details/<pk>", views.CustomerDetail.as_view(), name="customer_details"),
    # path("add_customer", views.AddCustomer.as_view(), name="add_customer"),
    # path("update_customer/<pk>", views.UpdateCustomer.as_view(), name="update_customer"),
    # path("delete_customer/<pk>", views.DeleteCustomer.as_view(), name="delete_customer"),
    path("products/", views.products, name="products"),
    path("product_details/<pk>", views.product_details, name="product_details"),
    path("user/", views.UserPage, name="user_page"),
    path("customers/<str:pk_test>/", views.customer, name="customers"),
    path("create_order/<str:pk>", views.createOrder, name="create_order"),
    path("update_order/<str:pk>", views.UpdateOrder, name="update_order"),
    path("delete_order/<str:pk>", views.deleteOrder, name="delete_order"),
    path("login", views.login_page, name="login"),
    path("logout", views.logout_user, name="logout"),
    path("register", views.register_page, name="register"),

]
