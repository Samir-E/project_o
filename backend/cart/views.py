from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_201_CREATED

from .serializers import *
from .models import *


# Create your views here.
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Orders.objects.all().order_by('-id')
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        pass


class OrderPositionViewSet(viewsets.ModelViewSet):
    queryset = OrderPosition.objects.all().order_by('-id')
    serializer_class = OrderPositionSerializer


class PositionInOrderViewSet(viewsets.ModelViewSet):
    queryset = PositionInOrder.objects.all().order_by('-id')
    serializer_class = PositionInOrderSerializer

# class CartTotalPriceView(GenericAPIView):
#     """
#     Вывод итоговой суммы заказа
#     """
#
#     def get(self, request):
#         status_code = HTTP_200_OK
#         data = {}
#         # user = request.user
#         # if not user:
#         #     status_code = HTTP_400_BAD_REQUEST
#         #     data = {
#         #         'status_code': status_code,
#         #         'message': 'Пользователь не авторизован'
#         #     }
#         try:
#             cart = Cart.objects.filter(user=request.user).first()
#             data['total_price'] = cart.get_total()
#         except Exception as e:
#             print(str(e))
#             status_code = HTTP_400_BAD_REQUEST
#         finally:
#             return Response(data, status=status_code)


# class RetrieveDestroyCartView(RetrieveDestroyAPIView):
#     """
#     Извлечение или удаление корзины. Этот API будет использоваться для
# просмотра корзины или ее опустошения
#     """
#
#     serializer_class = CartSerializer
#     permission_classes = IsAuthenticated(),
#
#     def get_object(self):
#         cart, created = Cart.objects.get_or_create(user=self.request.user)
#         return cart
#
#
# class AddItemToCartView(CreateAPIView):
#     """Добавление товара в корзину"""
#
#     def create(self, request, *args, **kwargs):
#         user = request.user
#
#         if user:
#             cart, created = Cart.objects.get_or_create(user=user)
#         else:
#             return Response({"error": True,
#                              "message": "Недостаточно информации "
#                                         "для создания корзины."})
#
#         item = cart.search_item(self.request.data['position'])
#         cart.add_item(position=self.request.data['position'],
#                       servings=self.request.data['servings']) \
#             if item is None else item.update_servings(self.request.data['servings'])
#         return Response(CartSerializer(cart).data, status=HTTP_201_CREATED)
#
#
# class RemoteItemFromCartView(GenericAPIView):
#     """Удаление товара из корзины"""
#
#     serializer_class = RemoveItemFromCartSerializer
#     permission_classes = IsAuthenticated(),
#     # authentication_classes = (TokenAuthentication,
#     #                           SessionAuthentication)
#
#     def post(self, request, *args, **kwargs):
#         user = request.user
#
#         if user.is_authenticated:
#             cart, created = Cart.objects.get_or_create(user=user)
#         else:
#             return Response({"error": True,
#                              "message": "Недостаточно информации "
#                                         "для создания корзины."})
#
#         item = cart.search_item(self.request.data['position'])
#         item.delete() if item is not None else None
#         return Response(CartSerializer(cart).data, status=HTTP_200_OK)


# def created_order(self, request, *args, **kwargs):
#     data = Cart.objects.filter(id = sefl .request.)
