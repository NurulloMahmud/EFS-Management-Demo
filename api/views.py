from rest_framework.views import APIView
from .serializers import EFSSerializer
from main.models import Efs
from rest_framework.response import Response


class GenerateEFScodeAPIView(APIView):
    def post(self, request):
        serialized_data = EFSSerializer(data=request.data)
        if serialized_data.is_valid(raise_exception=True):
            serialized_data.save()
            return Response(data=serialized_data.data)
        else:
            return Response(status=400)