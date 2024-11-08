from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from notification_be.apps.models_container import Product
from notification_be.apps.permissions import IsShop, IsAdmin, IsAuthenticated
from rest_framework import parsers, renderers
from notification_be.apps.views_container import status
from rest_framework.pagination import LimitOffsetPagination
from notification_be.apps.serializers_container import AddProductSerializer, ListProductSerializer, UpdateProductSerializer


class AddProductViewAPI(APIView):
    permission_classes = [IsShop]
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.FileUploadParser)
    renderer_classes = (renderers.JSONRenderer,)

    @swagger_auto_schema(request_body=AddProductSerializer)
    def post(self, request):
        serializer = AddProductSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ListProductAPIView(APIView):
    permission_classes = [IsShop]

    def get(self, request):
        if IsAdmin().has_permission(request, self):
            products = Product.objects.all()
        elif IsShop().has_permission(request, self):
            products = Product.objects.filter(user=request.user)
        else:
            return Response({"error": "You do not have access."}, status=status.HTTP_403_FORBIDDEN)

        serializer = ListProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UpdateProductViewAPI(APIView):
    permission_classes = [IsShop]
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.FileUploadParser)
    renderer_classes = (renderers.JSONRenderer,)

    def get_object(self, pk):
        try:
            return Product.objects.get(pk = pk)
        except Product.DoesNotExist:
            return None

    @swagger_auto_schema(
        operation_description="Update all product information using UUID",
        request_body=UpdateProductSerializer
    )
    def put(self, request, pk):
        product = self.get_object(pk)
        if not product:
            return Response({"error": "Product does not exist."}, status=status.HTTP_404_NOT_FOUND)
        serializer = UpdateProductSerializer(product, data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        product = self.get_object(pk)
        if not product:
            return Response({"error": "Product does not exist."}, status=status.HTTP_404_NOT_FOUND)
        if product.user != request.user:
            return Response({"error": "You do not have permission to delete this product."}, status=status.HTTP_403_FORBIDDEN)

        product.delete()
        return Response({"message": "Product delete successful."}, status=status.HTTP_200_OK)

class SearchProductAPIView(APIView):
    permission_classes = [IsAuthenticated]

    id_param = openapi.Parameter('id', openapi.IN_QUERY, description="The product's UUID", type=openapi.TYPE_STRING)
    name_param = openapi.Parameter('name', openapi.IN_QUERY, description="Product name", type=openapi.TYPE_STRING)
    price_param = openapi.Parameter('price', openapi.IN_QUERY, description="Price of the product", type=openapi.TYPE_NUMBER)

    @swagger_auto_schema(manual_parameters=[id_param, name_param, price_param])
    def get(self, request):
        products = Product.objects.all()
        product_id = request.query_params.get('id', None)
        name = request.query_params.get('name', None)
        price = request.query_params.get('price', None)

        if product_id:
            products = products.filter(id=product_id)
        if name:
            products = products.filter(name__icontains=name)
        if price:
            products = products.filter(price=price)

        if not products.exists():
            return Response({"message": "There are no products that meet the search criteria."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ListProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ListProductOffsets(APIView, LimitOffsetPagination):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        products = Product.objects.all()
        results = self.paginate_queryset(products, request, view=self)
        serializer = ListProductSerializer(results, many=True)
        return self.get_paginated_response(serializer.data)