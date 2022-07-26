from django.contrib.auth import get_user_model
from django.utils.timezone import now as timezone_now
from django.core.exceptions import ValidationError
from rest_framework import generics, permissions, response, authentication, status
from constance import config

User = get_user_model()

from account.serializers import UserSerializer, UserDetailSerializer
from account import permissions as custom_permissions

from .utils import perform_raise_permission
from .models import PaidOrder, DeviceToken
from .serializers import (
    DeviceTokenModelSerializer, 
    OrderModelSerializer, 
    VerifyDeviceTokenSerializer, 
    DeviceAddPluginSerialzier,
    DeviceInfoSerializer,
)
class ReplicaOrderCreateAPIView(generics.CreateAPIView):
    serializer_class = OrderModelSerializer
    authentication_classes = []
    permission_classes = [permissions.AllowAny,]
    queryset = PaidOrder.objects.all()


class DeviceTokenCreateAPIView(generics.CreateAPIView):
    serializer_class = DeviceTokenModelSerializer
    authentication_classes = [authentication.TokenAuthentication,]
    permission_classes = [permissions.IsAuthenticated]
    queryset = DeviceToken.objects.all()


class DeviceTokenAddPlugin(generics.CreateAPIView):
    serializer_class = DeviceAddPluginSerialzier
    authentication_classes = [authentication.TokenAuthentication,]
    permission_classes = [permissions.IsAuthenticated,]


class DeviceTokenVerifyAPIView(generics.GenericAPIView):
    serializer_class = VerifyDeviceTokenSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated,]
    queryset = DeviceToken.objects.all()

    def post(self, request, *args, **kargws):
        sered = self.serializer_class(data=request.data, context={"request": request})
        if sered.is_valid():
            return response.Response(
                {
                    "permission": sered.validate_the_token(validated_data=sered.validated_data), 
                    "success": True,
                }
            )
        else:
            return response.Response(
                {"permission": False, "success": True}
            )


class TestOptionsAPIView(generics.GenericAPIView):
    serializer_class = OrderModelSerializer
    authentication_classes = []
    permission_classes = [permissions.AllowAny,]

    def post(self, request):
        print(request.data)
        try:
            print(request.META)
        except Exception as E:
            print(E)
        return response.Response({"status": "OK"}, status=status.HTTP_200_OK)
    
    def get(self, request):
        print(request)
        return response.Response({"status": "OK"}, status=status.HTTP_200_OK)


class OrderUpdatePaymentStatusView(generics.GenericAPIView):
    serializer_class = OrderModelSerializer
    authentication_classes = []
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        if request.data.get("status") == "paid":
            try:
                target_order = PaidOrder.objects.get(wp_order_id=request.data.get("id"))
                perform_raise_permission(target_order, customer_id=request.data.get("customer_id"))
                return response.Response(
                    data={"msg": "OK"},
                    status=status.HTTP_200_OK
                )
            except PaidOrder.DoesNotExist:
                print("The order has not been submitted")
                return response.Response(
                    data={"msg": "The order has not been added to the api"},
                    status=status.HTTP_400_BAD_REQUEST,
                )


class DeviceCreateOrVerify(generics.GenericAPIView):
    serializer_class = DeviceTokenModelSerializer
    authentication_classes = [authentication.TokenAuthentication,]
    permission_classes = [permissions.IsAuthenticated,]

    def post(self, request, *args, **kwargs):

        # checks if the request has token or empty
        if request.data.get("token") == "" or None:
            # validate user perms and create token
            device_token = request.user.create_device(product_id=request.data.get("product_id"))
            if device_token:
                device_token.device_uuid = request.data.get('uuid')
                device_token.save()
            plugins = device_token.activate_and_handle_plugins()
            if device_token:
                data = {
                    "device-token": device_token.token,
                    "plugins": [plugin[0] for plugin in device_token.plugins.all().values_list("wp_product_id")],
                    "userproductspermissions": UserDetailSerializer(request.user).data["product_permissions"],
                    "first-create": True,
                }
                message = "Successfully created device token for user."
                status_code = status.HTTP_201_CREATED
        else:
            # validate ser perms and verify token
            try:
                # refresh token by time
                device_token = DeviceToken.objects.get(token=request.data.get("token"))
                if request.data.get("uuid") == device_token.device_uuid:
                    t = (timezone_now() - device_token.refresh_time)
                    if t.seconds > 3600*config.TOKEN_EXPIRATION_HOURS or t.days > 0 or device_token.expired:
                        d_token = device_token.refresh_token()
                        print(d_token)
                        # validate device with unique data
                        message = "Successfully refreshed device token."
                        status_code = status.HTTP_200_OK
                    else:
                        message = "Successfully validated token."
                        status_code = status.HTTP_200_OK
                        d_token = None
                    # take care of unactivate 
                    plugins = device_token.activate_and_handle_plugins()
                    print("did the plugin update \n")
                    data = {
                        "device-token": device_token.token,
                        "plugins": [plugin[0] for plugin in device_token.plugins.all().values_list("wp_product_id")],
                        "userproductspermissions": UserDetailSerializer(request.user).data["product_permissions"],
                        "first-create": False,
                    }
                else:
                    message = "The device is not correct."
                    status_code = status.HTTP_401_UNAUTHORIZED
                    data = {
                        "device-token": "",
                        "first-create": False,
                        "plugins": None,
                        "userproductspermissions": None, 
                    }
            except DeviceToken.DoesNotExist:
                message = "Token is wrong, please request with a different token."
                status_code = status.HTTP_401_UNAUTHORIZED
                data = {
                    "device-token": "",
                    "first-create": False,
                    "plugins": [],
                    "userproductspermissions": [],
                }
            except ValidationError:
                message = "Token is wrong, lpease request with a different token."
                status_code = status.HTTP_401_UNAUTHORIZED
                data = {
                    "device-token": "",
                    "first-create": False,
                    "plugins": None,
                    "userproductspermissions": None, 
                }
        data["message"] = message
        return response.Response(data=data, status=status_code)
            
class DeviceExpireAPIView(generics.GenericAPIView):
    serializer_class = DeviceTokenModelSerializer
    authentication_classes = [authentication.TokenAuthentication,]
    permission_classes = [
        permissions.IsAuthenticated,
        custom_permissions.DevicePermission,
    ]

    def post(self, request):
        try:
            if request.data.get("token"):
                try:
                    device_token = DeviceToken.objects.get(token=request.data.get("token"))
                    device_token.expired = True
                    device_token.save()
                    message = "Successfully expired the device token."
                    status_code = status.HTTP_200_OK
                except DeviceToken.DoesNotExist:
                    message = "Wrong token"
                    status_code = status.HTTP_401_UNAUTHORIZED
            else:
                message = "Enter the token with your request"
                status_code = status.HTTP_401_UNAUTHORIZED
        except KeyError:
            message = "Provide the necessary data."
            status_code = status.HTTP_400_BAD_REQUEST
        return response.Response(data = {"message": message}, status=status_code)
