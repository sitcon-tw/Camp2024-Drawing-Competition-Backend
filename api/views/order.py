from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth.models import User
from api.model.order import Order
from api.model.part import Part
from api.model.order_detail import OrderDetail
from api.serializers.order import OrderSerializer, CreateOrderSerializer
from drf_yasg.utils import swagger_auto_schema


class OrderViewSet(viewsets.GenericViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def find_all(self, request, *args, **kwargs):
        serializer = OrderSerializer(Order.objects.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=CreateOrderSerializer)
    def add(self, request, *args, **kwargs):
        serializer = CreateOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Part
        part_id_list = serializer.validated_data["part_id_list"]
        part_number_list = serializer.validated_data["part_number_list"]
        for id, num in zip(part_id_list, part_number_list):
            part = Part.objects.get(id=id)
            if part.number < num:
                return Response(
                    {"error": "Not enough part"}, status=status.HTTP_400_BAD_REQUEST
                )
            else:
                part.number -= num
                part.save()
        # Create Order Detail
        for id, num in zip(part_id_list, part_number_list):
            order_detail = OrderDetail.objects.create(
                number=num,
                part_id=Part.objects.get(id=id),
                order_number=serializer.validated_data["order_number"],
            )
            order_detail.save()
        # Create Order
        order = Order.objects.create(
            order_number=serializer.validated_data["order_number"],
            description=serializer.validated_data["description"],
            status=serializer.validated_data["status"],
            expected_date=serializer.validated_data["expected_date"],
            user_id=User.objects.get(username=serializer.validated_data["username"]),
        )
        order.save()
        return Response({"message": "Order created"}, status=status.HTTP_201_CREATED)


class OrderOperateViewSet(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderScheduleViewSet(APIView):
    def get(self, request):
        order = Order.objects.all().filter(status="待處理").order_by("expected_date")
        serializer = OrderSerializer(order, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
