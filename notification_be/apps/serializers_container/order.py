from notification_be.apps.serializers_container import serializers, Cart, Product,Order,ProductSerializer,UserSerializer,ListCartSerializer
from rest_framework.exceptions import ValidationError
from django.db.models import Sum
from  notification_be.apps.enum_container import  Status
from notification_be.apps.utils.notification_service import NotificationService
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class ListOrderSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    user = UserSerializer()
    cart = ListCartSerializer()
    class Meta:
        model = Order
        fields = ['product', 'user', 'cart','total_amount']


class AddOrderSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), required=False)
    cart = serializers.PrimaryKeyRelatedField(queryset=Cart.objects.all(), many=True, required=False)

    class Meta:
        model = Order
        fields = ['product', 'cart']

    def create(self, validated_data):
        user = self.context['request'].user
        if 'cart' in validated_data and validated_data['cart'] and 'product' in validated_data:
            raise ValidationError("Bạn không thể cung cấp cả sản phẩm và giỏ hàng cùng một lúc.")
        if 'product' in validated_data and validated_data['product']:
            product = validated_data['product']
            order = Order(user=user, product=product, total_amount=product.price)
            order.save()  # Lưu order trước khi liên kết cart
            NotificationService.notify_new_order(
                user_id=user,
                order_id=order.id,
                price=product.price,
                device_token=product.user.device_token,
                recipient= product.user,
                username =user.username
            )
        else:
            user_carts = Cart.objects.filter(user=user,status=Status.PENDING.value)
            if not user_carts.exists():
                raise ValidationError("Người dùng không có giỏ hàng nào.")
            total_amount = user_carts.aggregate(Sum('total_money'))['total_money__sum'] or 0
            if total_amount <= 0:
                raise ValidationError("Tổng tiền trong giỏ hàng của người dùng bằng 0, không thể đặt hàng.")
            order = Order(user=user, total_amount=total_amount)
            order.save()
            for cart in user_carts:
                product = cart.product
                owner_device_token = product.user.device_token
                NotificationService.notify_new_order(
                    user_id=user,
                    order_id=order.id,
                    price=product.price,
                    device_token=owner_device_token,
                    recipient=product.user,
                    username=user.username,
                )
            order.cart.set(user_carts)
            user_carts.update(status=Status.ORDERED.value)

        return order