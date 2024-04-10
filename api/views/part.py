from rest_framework import generics
from api.model.part import Part
from api.serializers.part import PartSerializer

class PartListCreateViewSet(generics.ListCreateAPIView):
    queryset = Part.objects.all()
    serializer_class = PartSerializer

class PartRetrieveUpdateDestroyViewSet(generics.RetrieveUpdateDestroyAPIView):
    queryset = Part.objects.all()
    serializer_class = PartSerializer