from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("car/", include('car.urls')),
    #path("review/", include('review.urls')),
    path("orders/", include('orders.urls')),
    path("account/", include('account.urls')),
    path("account-profile/", include('account_profile.urls')),
    path("cart/", include('cart.urls')),
    path("kakao-oauth/", include('kakao_oauth.urls')),
    path("authentication/", include('authentication.urls')),
    path("payments/", include('payments.urls')),
    path("excel/", include('excel.urls')),
    path("board/", include('board.urls')),
]
