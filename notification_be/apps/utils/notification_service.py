from .firebase_client import FirebaseClient
from notification_be.apps.models_container.notification import Notification
from notification_be.apps.enum_container.notification_type import NotificationType
class NotificationService:
    @staticmethod
    def notify_new_product(user_id, product_id, product_name, price, device_token, recipient):
        notification_type = NotificationType.PRODUCT.value
        message_data = {
            "message": f"Sản phẩm mới '{product_name}' đã được tạo.",
            "product_id": str(product_id),
            "product_name": product_name,
            "price": str(price)
        }
        # Gửi thông báo qua Firebase
        return NotificationService.send_firebase_notification(user_id, product_id, notification_type, message_data, device_token, recipient)


    @staticmethod
    def notify_new_order(user_id, order_id, price, device_token,username,recipient):
        notification_type = NotificationType.ORDER.value
        message_data = {
            "message": f"Bạn có đơn hàng mới từ {username}",
            "order_id": str(order_id),
            "price": str(price)
        }
        return NotificationService.send_firebase_notification(user_id, order_id, notification_type, message_data,device_token,recipient)
    @staticmethod
    def send_firebase_notification(user_id, object_type_id, notification_type, data, device_token,recipient):
        # Tạo đối tượng Notification

        notification = Notification.objects.create(
            user=user_id,
            object_type_id=object_type_id,
            notification_type=notification_type,
            recipient=recipient,
            data=data
        )

        # Khởi tạo FirebaseClient và gọi phương thức send_notification
        firebase_client = FirebaseClient()
        response = firebase_client.send_notification(
            notification=notification,
            device_token=device_token
        )
        return response