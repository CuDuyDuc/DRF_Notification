from notification_be.apps.serializers_container import UserSerializer, Product, serializers, User
from notification_be.apps.utils.notification_service import NotificationService
from notification_be.apps.permissions import UserRole

class AddProductSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=True)

    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'price', 'quantity']

    def create(self, validated_data):
        user = self.context['request'].user
        product = Product(user = user, **validated_data)
        product.save()
        admin = User.objects.filter(role=UserRole.ADMIN.value).first()
        if admin:
            # Gửi thông báo cho Admin
            NotificationService.notify_new_product(
                user_id=user,
                product_id=product.id,
                product_name=product.name,
                price=product.price,
                device_token=admin.device_token,
                recipient=admin
            )
        return product

class UpdateProductSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)

    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'price', 'quantity']

    def update(self, instance, validated_data):
        user = self.context['request'].user
        if instance.user != user:
            raise serializers.ValidationError("You do not have permission to repair this product.")
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class ListProductSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'image', 'price', 'quantity', 'user']