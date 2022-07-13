from django import template
from food_store.models import Order

register = template.Library()

@register.filter(name="cart_item_count")
def cart_item_count(user):
    if user.is_authenticated:
        qs = Order.objects.filter(user=user, ordered=False)
        if qs.exist():
            return qs[0].items.count
    else:
        return 0