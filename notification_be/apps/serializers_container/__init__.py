from notification_be.apps.models_container import User, Product, Cart, Order
from rest_framework import serializers, status
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import jwt
from django.utils.encoding import force_str
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from notification_be.apps.serializers_container.user import *
from notification_be.apps.serializers_container.product import *
from notification_be.apps.serializers_container.cart import *
from notification_be.apps.serializers_container.order import *