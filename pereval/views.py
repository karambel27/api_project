from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import PerevalSerializer


class SubmitDataAPIView(APIView):
    def post(self, request):
        serializer = PerevalSerializer(data=request.data)

        if serializer.is_valid():
            try:
                pereval = serializer.save()
                return Response(
                    {
                        'status': 200,
                        'message': None,
                        'id': pereval.id,
                    },
                    status=status.HTTP_200_OK
                )

            except Exception as error:
                return Response(
                    {
                        'status': 500,
                        'message': str(error),
                        'id': None,
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        return Response(
            {
                'status': 400,
                'message': serializer.errors,
                'id': None,
            },
            status=status.HTTP_400_BAD_REQUEST
        )
