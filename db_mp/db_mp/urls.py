from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),

    path("rent_car/", include('rent_car.urls')),
    path("rent_car_review/", include('rent_car_review.urls')),

    path("account/", include('account.urls')),
    path("account-profile/", include('account_profile.urls')),
    path("cart/", include('cart.urls')),

]
