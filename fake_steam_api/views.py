from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import ListView, TemplateView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Item, Trade
from .serializers import TradeSerializer

User = get_user_model()


class ItemListView(LoginRequiredMixin, ListView):
    model = Item
    template_name = "item_list.html"

    def get_queryset(self):
        user = self.request.user
        return Item.objects.filter(owner=user)


class HomePageView(TemplateView):
    template_name = "home.html"


class TradeListView(LoginRequiredMixin, ListView):
    model = Trade
    template_name = "trade_list.html"
    context_object_name = "trades"

    def get_queryset(self):
        user = self.request.user
        return Trade.objects.filter(buyer=user) | Trade.objects.filter(seller=user)


class TradeOfferCreateView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        items = Item.objects.exclude(owner=request.user)  # 列出其他用户的 Items
        return render(request, "trade_offer_form.html", {"items": items})

    def post(self, request, *args, **kwargs):
        item_id = request.POST.get("item")
        try:
            item = Item.objects.get(id=item_id)
            Trade.objects.create(
                buyer=request.user,
                seller=item.owner,  # 购买的物品的拥有者是卖家
                trade_item=item,
                status="P",
            )
            return redirect("trade_list")
        except Item.DoesNotExist:
            return HttpResponseForbidden("Invalid item")


class TradeActionView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        trade_id = request.POST.get("trade_id")
        action = request.POST.get("action")
        trade = get_object_or_404(Trade, id=trade_id)

        if action == "cancel" and trade.buyer == request.user:
            trade.status = "C"
            trade.save()
        elif action == "reject" and trade.seller == request.user:
            trade.status = "R"
            trade.save()
        elif action == "accept" and trade.seller == request.user:
            trade.status = "A"
            trade.save()
            trade.trade_item.owner = trade.buyer
            trade.trade_item.save()
        else:
            return HttpResponseForbidden("Invalid action or permissions")

        return redirect("trade_list")


class TradeStatusAPIView(APIView):
    def get(self, request, trade_id):
        try:
            trade = Trade.objects.get(id=trade_id)
        except Trade.DoesNotExist:
            return Response(
                {"error": "Trade not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = TradeSerializer(trade)
        return Response([serializer.data])


