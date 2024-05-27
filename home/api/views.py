from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from home.api.serializers import CrashReportSerializer


class BuildPdfAPIView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = CrashReportSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
