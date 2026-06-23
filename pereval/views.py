from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import PerevalAdded
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

    def get(self, request, pk=None):
        if pk is not None:
            try:
                pereval = PerevalAdded.objects.get(pk=pk)
            except PerevalAdded.DoesNotExist:
                return Response(
                    {
                        'message': 'Запись не найдена.'
                    },
                    status=status.HTTP_404_NOT_FOUND
                )

            serializer = PerevalSerializer(pereval)

            return Response(serializer.data)

        email = request.query_params.get('user__email')

        if email:
            perevals = PerevalAdded.objects.filter(user__email=email)
            serializer = PerevalSerializer(perevals, many=True)

            return Response(serializer.data)

        return Response(
            {
                'message': 'Укажите id записи или user__email.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    def patch(self, request, pk=None):
        if pk is None:
            return Response(
                {
                    'state': 0,
                    'message': 'Не указан id записи.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            pereval = PerevalAdded.objects.get(pk=pk)
        except PerevalAdded.DoesNotExist:
            return Response(
                {
                    'state': 0,
                    'message': 'Запись не найдена.'
                },
                status=status.HTTP_404_NOT_FOUND
            )

        if pereval.status != 'new':
            return Response(
                {
                    'state': 0,
                    'message': 'Редактировать можно только записи со статусом new.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = PerevalSerializer(
            pereval,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()

            return Response(
                {
                    'state': 1,
                    'message': None
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                'state': 0,
                'message': serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )