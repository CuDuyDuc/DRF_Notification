from notification_be.apps.serializers_container import serializers, Cart, Product
from rest_framework.exceptions import ValidationError
from  notification_be.apps.enum_container import Status
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ListCartSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = Cart
        fields = ['product', 'user', 'quantity','status']


class AddCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['product', 'quantity']

    def create(self, validated_data):
        return self._update_or_create_cart_item(validated_data)

    def _update_or_create_cart_item(self, validated_data):
        id_product = validated_data.get('product')
        user = self.context['request'].user
        quantity = validated_data.get('quantity', 1)
        try:
            cart_item = Cart.objects.get(product=id_product, user=user, status=Status.PENDING.value)
            cart_item.quantity += quantity
        except Cart.DoesNotExist:
            cart_item = Cart(product=id_product, user=user, quantity=quantity, status=Status.PENDING.value)
        cart_item.total_money = cart_item.quantity * cart_item.product.price
        cart_item.save()

        return cart_item

class UpdateCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['quantity']

    def update(self, instance, validated_data):
        if instance.status != Status.PENDING.value:
            raise ValidationError("Không thể cập nhật giỏ hàng khi trạng thái không phải là PENDING.")

        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.total_money = instance.quantity * instance.product.price
        instance.save()
        return instance
