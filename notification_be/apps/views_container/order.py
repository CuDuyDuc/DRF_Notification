from rest_framework.views import APIView
from notification_be.apps.permissions import IsUser
from drf_yasg.utils import swagger_auto_schema
from rest_framework import renderers, parsers
from notification_be.apps.views_container import AddOrderSerializer,status, Response


class AddOrderViewAPI(APIView):
    permission_classes = [IsUser]
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.FileUploadParser)
    renderer_classes = (renderers.JSONRenderer,)

    @swagger_auto_schema(
        request_body=AddOrderSerializer,
        responses={201: "Thêm thành công"}
    )
    def post(self, request):
        serializer = AddOrderSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'message': 'Thêm thành công',
            'data': serializer.data  # Trả về dữ liệu đã lưu
        }, status=status.HTTP_201_CREATED)