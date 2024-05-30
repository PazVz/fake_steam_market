from django.contrib.auth import views as auth_views
from django.urls import path

from .views import (
    HomePageView,
    ItemListView,
    TradeActionView,
    TradeListView,
    TradeOfferCreateView,
    TradeStatusAPIView,
)

urlpatterns = [
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("item_list/", ItemListView.as_view(), name="item_list"),
    path("trades/", TradeListView.as_view(), name="trade_list"),
    path(
        "trade_offer/create/", TradeOfferCreateView.as_view(), name="trade_offer_create"
    ),
    path("trade_action/", TradeActionView.as_view(), name="trade_action"),
    path("", HomePageView.as_view(), name="home"),
    path(
        "api/trade_status/<int:trade_id>/",
        TradeStatusAPIView.as_view(),
        name="trade_status_api",
    ),
]
