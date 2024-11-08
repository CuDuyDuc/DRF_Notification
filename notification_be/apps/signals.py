from django.db import OperationalError
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from notification_be.apps.models_container.user import User
from django.contrib.auth.hashers import make_password

@receiver(post_migrate)
def create_admin_user_if_not_exists(sender, **kwargs):
    try:
        if sender.name == 'notification_be.apps':
            if not User.objects.filter(email='admin@admin.com').exists():
                user = User(
                    email = 'admin@admin.com',
                    username = 'admin',
                    fullname = 'Admin',
                    password = make_password('admin123'),
                    is_active = True,
                    role = 'ADMIN'
                )
                user.save()
                print('Admin user create successfully.')
    except OperationalError:
        print('Database is not ready yet.')
    except Exception as e:
        print(f'An error occurred: {e}')