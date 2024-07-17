from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from api.serializers.clip import ClipRequestDTO, ClipResponseDTO
from api.utils.clip_instance import Clip
from api.utils.ssim_instance import SSIM

clip_instance = Clip.get_instance()
ssim_instance = SSIM.get_instance()

class ClipAPIView(APIView):
    @swagger_auto_schema(
        request_body=ClipRequestDTO,
        response={200: ClipResponseDTO},
    )
    def post(self,request):
        image1_path = request.data.get("image1_path")
        image2_path = request.data.get("image2_path")
        # clip_instance = Clip().get_instance()
        clip_instance = SSIM.get_instance()

        # similarity =clip_instance.calculate_clip_similarity(image1_path, image2_path)
        similarity =clip_instance.calculate_similarity(image1_path, image2_path)

        return Response({
            "similarity": similarity
        }, status=status.HTTP_200_OK)
