from api.model.order import Order
from api.model.part import Part
from api.model.order_detail import OrderDetail
from django.contrib.auth.models import User
from rest_framework import serializers

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class CreateOrderSerializer(serializers.Serializer):
    order_number = serializers.CharField()
    description = serializers.CharField()
    status = serializers.CharField()
    username = serializers.CharField()
    expected_date = serializers.DateTimeField()
    # For Order Detail
    part_id_list = serializers.ListField(child=serializers.IntegerField())
    part_number_list = serializers.ListField(child=serializers.IntegerField())
    def create(self, validated_data):
        user_id = User.obejcts.get(username=validated_data['username']).id  
        order = Order.objects.create(
            order_number=validated_data['order_number'],
            description=validated_data['description'],
            status=validated_data['status'],
            expected_date=validated_data['expected_date'],
            user_id=user_id
        )
        return order