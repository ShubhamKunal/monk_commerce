from django.urls import path
from . import views

urlpatterns = [
    path("", views.get_coupons, name="get_coupons"),
    path("<int:id>/", views.edit_coupon, name="edit_coupon" ),
]
