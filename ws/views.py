from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .serializers import VistoriaSerializer
from django.contrib.auth import authenticate
from relatorios.models import Vistoria
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
import json
from django.core import serializers
from django.contrib.auth.models import User

# Create your views here.
@csrf_exempt
def loginmobile(request):
	if request.method == 'POST':
		name = request.POST['name']
		password = request.POST['password']
		user=authenticate(username=name, password=password)

		data = None
		if user is not None:
			data = {
				"id": user.id,
				"status": 200
			}
		else:
			data = {
				"status": 404
			}
		return JsonResponse(data)




@csrf_exempt
def cadastrovistoria(request):

	if request.method == 'GET':
		vistorias = Vistoria.objects.all()
		serializer = VistoriaSerializer(vistorias, many=True)
		jason = json.dumps(serializer.data)
		print(jason)

		return JsonResponse(jason, safe=False)

	if request.method == 'POST':
		data = json.loads(request.body.decode("UTF-8"))
		user = User.objects.get(id = data.get('autor'))
		serializerVistoria = VistoriaSerializer(data=data)
		if serializerVistoria.is_valid():
			print(serializerVistoria)
			serializerVistoria.save()
			return JsonResponse(serializerVistoria.data)
		return JsonResponse(serializerVistoria.errors, status=400)
