from rest_framework import generics, authentication, permissions, response, status

from . import ProductType
from .models import Product
from .serializers import PluginSerializer, ProductSerializer
from order.models import DeviceToken

from account import permissions as custom_permissions

class ProductReplicaCreateAPIView(generics.CreateAPIView):
    authentication_classes = []
    permission_classes = [permissions.AllowAny,]
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    
class ProductRetrieveAPIVIew(generics.GenericAPIView):
    serializer_class = ProductSerializer
    authentication_classes = [authentication.TokenAuthentication,]
    permission_classes = [
        permissions.IsAuthenticated, 
        custom_permissions.DevicePermission,
        custom_permissions.UserAgentPermission,
    ]

    def get(self, request, wp_product_id, *args, **kwargs):
        product = request.user.products.all().filter(
            wp_product_id=wp_product_id,
            product_type=ProductType.NORMAL
        )
        device_token = DeviceToken.objects.get(token=request.data.get("token"), device_uuid=request.data.get("uuid"))
        if product.exists():
            return response.Response(
                {
                    "proudct": ProductSerializer(product.first()).data,
                    "plugins": PluginSerializer(
                                    device_token.plugins.all(), 
                                    many=True
                                ).data
                }, status=status.HTTP_200_OK
            )
        else:
            return response.Response(
                {"message": "Can't find that product"},
                status=status.HTTP_404_NOT_FOUND,
            )
            