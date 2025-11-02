from django.urls import path
from . import views

urlpatterns = [
    path("", views.get_carts, name="get_carts"),
    path("<int:id>/", views.get_cart, name="get_cart"),
    path("update/", views.add_product_in_cart, name="add_product_in_cart"),
    path("create/", views.create_cart, name="create_cart"),
]
