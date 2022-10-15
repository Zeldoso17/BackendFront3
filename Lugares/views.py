import os
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import requests

from dotenv import load_dotenv
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, permissions, authentication

# Create your views here.

load_dotenv()
TOKEN = os.getenv('API_TOKEN')

@method_decorator(csrf_exempt, name='dispatch')
class getPlaces(APIView):

    authentication_classes = [ authentication.TokenAuthentication ]
    permission_classes = [ permissions.IsAuthenticated ]

    def get(self, request, query):
        try:
            urlApiBusqueda = f'https://www.inegi.org.mx/app/api/denue/v1/consulta/buscar/{query}/{ request.query_params["proximity"] }/{ request.query_params["metros"] }/{TOKEN}'
            print('PROXIMIDAD -> ', request.query_params["proximity"])
            locales = requests.get(urlApiBusqueda)
            data = {
                'message': 'Se encontraron resultados',
                'lugares': locales.json()
            }
            return Response(data, status=status.HTTP_200_OK)
        except:
            return Response({'message': "No se encontró ningun lugar cerca de ti"}, status=status.HTTP_404_NOT_FOUND)

@method_decorator(csrf_exempt, name='dispatch')
class getPlaceInfo(APIView):

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        try:
            urlApiBusqueda = f'http://www.inegi.org.mx/app/api/denue/v1/consulta/Ficha/{pk}/{TOKEN}'
            locales = requests.get(urlApiBusqueda)
            return Response(locales.json(), status=status.HTTP_200_OK)
        except:
            return Response("No se encontro informacion para ese lugar", status=status.HTTP_400_BAD_REQUEST)