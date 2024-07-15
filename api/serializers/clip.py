from rest_framework import serializers

class ClipRequestDTO(serializers.Serializer):
    image1_path = serializers.CharField()
    image2_path = serializers.CharField()

class ClipResponseDTO(serializers.Serializer):
    similarity = serializers.FloatField()