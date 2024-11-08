from notification_be.apps.serializers_container import UserSerializer, RegisterSerializer, LoginSerializer, CreateShopSerializer, AddCartSerializer, ListCartSerializer, UpdateCartSerializer, AddOrderSerializer
from notification_be.apps.models_container import User, Product, Cart
from rest_framework import status, renderers, parsers
from rest_framework.response import Response

from notification_be.apps.views_container.user import *
from notification_be.apps.views_container.product import *
from notification_be.apps.views_container.cart import *
from notification_be.apps.views_container.order import *