from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    wear = models.CharField(choices=[("FN", "Factory New"), ("MW", "Minimal Wear"), ("FT", "Field-Tested"), ("WW", "Well-Worn"), ("BS", "Battle-Scarred")], max_length=2)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="items")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Trade(models.Model):
    buyer = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="buyer_trades")
    seller = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="seller_trades")
    status = models.CharField(choices=[("P", "Pending"), ("A", "Accepted"), ("R", "Rejected"), ("C", "Canceled")], default="P", max_length=1)
    created_at = models.DateTimeField(auto_now_add=True)
    trade_item = models.ForeignKey(Item, on_delete=models.CASCADE)