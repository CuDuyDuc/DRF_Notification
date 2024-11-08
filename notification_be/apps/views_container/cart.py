from notification_be.apps.views_container import Cart, ListCartSerializer,status, Response, AddCartSerializer, UpdateCartSerializer
from notification_be.apps.permissions import IsUser
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from rest_framework import renderers, parsers
from rest_framework.generics import get_object_or_404
from notification_be.apps.enum_container import Status
class AddCartViewAPI(APIView):
    permission_classes = [IsUser]
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.FileUploadParser)
    renderer_classes = (renderers.JSONRenderer,)

    @swagger_auto_schema(
        request_body=AddCartSerializer,
        responses={201: "Thêm thành công"}
    )
    def post(self, request):
        serializer = AddCartSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'message': 'Thêm thành công',
            'data': serializer.data  # Trả về dữ liệu đã lưu
        }, status=status.HTTP_201_CREATED)


class ListCartViewAPI(APIView):
    permission_classes = [IsUser]
    renderer_classes = (renderers.JSONRenderer,)

    def get(self, request):
        user = request.user
        queryset = Cart.objects.filter(user=user, status=Status.PENDING.value)
        serializer = ListCartSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateCartViewAPI(APIView):
    permission_classes = [IsUser]
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.FileUploadParser)
    renderer_classes = (renderers.JSONRenderer,)

    def get_object(self, pk):
        return get_object_or_404(Cart, pk=pk, user=self.request.user)

    @swagger_auto_schema(
        operation_description="Cập nhật giỏ hàng bằng UUID và nhập dữ liệu trong body JSON",
        request_body=UpdateCartSerializer,
        responses={200: "Cập nhật thành công", 404: "Sản phẩm không tồn tại"}
    )
    def put(self, request, pk):
        cart_item = self.get_object(pk)
        serializer = UpdateCartSerializer(cart_item, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'message': 'Cập nhật giỏ hàng thành công',
            'data': serializer.data
        }, status=status.HTTP_200_OK)


class DeleteCartViewAPI(APIView):
    permission_classes = [IsUser]

    def get_object(self, pk):
        return get_object_or_404(Cart, pk=pk, user=self.request.user)

    def delete(self, request, pk):
        cart_item = self.get_object(pk)
        cart_item.delete()
        return Response({"message": "Xóa sản phẩm khỏi giỏ hàng thành công."}, status=status.HTTP_200_OK)