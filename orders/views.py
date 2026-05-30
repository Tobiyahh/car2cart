from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db import transaction
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views import View
from django.views.generic import TemplateView

from cart.models import Cart
from promotions.models import Coupon
from .models import Order, OrderItem


class CheckoutView(LoginRequiredMixin, View):
    template_name = 'orders/checkout.html'

    def get(self, request):
        cart = Cart.objects.filter(user=request.user).first()
        return render(request, self.template_name, {'cart': cart})

    def post(self, request):
        cart = Cart.objects.filter(user=request.user).first()
        if not cart or not cart.items.exists():
            return redirect('cart:detail')

        shipping_address = request.POST.get('shipping_address', '').strip()
        billing_address = request.POST.get('billing_address', '').strip()
        payment_method = request.POST.get('payment_method', 'cod')
        coupon_code = request.POST.get('coupon_code', '').strip().upper()

        if not shipping_address or not billing_address:
            messages.error(request, 'Please enter both shipping and billing addresses.')
            return render(request, self.template_name, {'cart': cart})

        with transaction.atomic():
            items = list(cart.items.select_related('product').select_for_update())
            for item in items:
                if item.quantity > item.product.stock:
                    messages.error(request, f'Only {item.product.stock} left for {item.product.title}.')
                    return redirect('cart:detail')

            subtotal = sum(item.total_price() for item in items)
            discount_amount = 0
            coupon = None
            if coupon_code:
                now = timezone.now()
                coupon = Coupon.objects.filter(active=True, code__iexact=coupon_code).first()
                if not coupon or (coupon.start_date and coupon.start_date > now) or (coupon.end_date and coupon.end_date < now):
                    messages.error(request, 'That coupon is not active.')
                    return render(request, self.template_name, {'cart': cart})
                discount_amount = subtotal * coupon.discount_percent / 100

            order = Order.objects.create(
                user=request.user,
                total_amount=subtotal - discount_amount,
                shipping_address=shipping_address,
                billing_address=billing_address,
                payment_method=payment_method,
                payment_status='pending' if payment_method == 'cod' else 'paid',
                coupon_code=coupon.code if coupon else '',
                discount_amount=discount_amount,
            )
            for item in items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    unit_price=item.product.price,
                )
                item.product.stock -= item.quantity
                item.product.save(update_fields=['stock'])
            cart.items.all().delete()
            request.session['latest_order_id'] = order.id
        return redirect('orders:confirmation')


class OrderHistoryView(LoginRequiredMixin, TemplateView):
    template_name = 'orders/history.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders'] = Order.objects.filter(user=self.request.user).order_by('-placed_at')
        return context


class OrderConfirmationView(LoginRequiredMixin, TemplateView):
    template_name = 'orders/confirmation.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_id = self.request.session.get('latest_order_id')
        context['order'] = Order.objects.filter(id=order_id, user=self.request.user).first()
        return context
