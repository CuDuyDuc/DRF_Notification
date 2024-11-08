import os
from firebase_admin import credentials, initialize_app, messaging, _apps

class FirebaseClient:
    def __init__(self):
        self._initialize_firebase_app()

    @staticmethod
    def _initialize_firebase_app():
        if not _apps:
            current_directory = os.getcwd()
            service_account_json = os.path.join(current_directory, 'notification-firebase-adminsdk.json')
            if not os.path.exists(service_account_json):
                raise FileNotFoundError("Tệp notification-firebase-adminsdk.json không tồn tại.")
            cred = credentials.Certificate(service_account_json)
            initialize_app(cred)

    @staticmethod
    def send_notification(notification, device_token: str = None):
        if not device_token:
            print("Không có device_token. Không thể gửi thông báo.")
            return None
        data_notification = {
            "title": f"{notification.notification_type} Notification",
            "body": f"{notification.data}"
        }
        print('lỗi dòng 28',notification)

        if device_token:
            notification_message = messaging.Notification(**data_notification)
            message = messaging.Message(notification=notification_message, token=device_token)
            response = messaging.send(message)
            return response
