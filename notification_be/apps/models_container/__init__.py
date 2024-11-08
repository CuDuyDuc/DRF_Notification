import uuid
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager, PermissionsMixin
from django.db import models

from notification_be.apps.models_container.user import User
from notification_be.apps.models_container.product import Product
from notification_be.apps.models_container.cart import Cart
from notification_be.apps.models_container.notification import Notification
from notification_be.apps.models_container.order import Order