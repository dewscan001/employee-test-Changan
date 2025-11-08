from django.http.response import JsonResponse, HttpResponse
from .models import *
from .serializers import *
from rest_framework.parsers import JSONParser
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

# Create your views here.
@csrf_exempt
@require_http_methods(["GET", "POST"])
@login_required
def position_list(request):
    if request.method == "GET":
        positionModel = PositionModel.objects.all()
        serializer = PositionSerializer(positionModel, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == "POST":
        data = JSONParser().parse(request)
        serializer = PositionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        else:
            return JsonResponse(serializer.errors, status=400)

@csrf_exempt
@require_http_methods(["GET", "POST"])
@login_required
def department_list(request):
    if request.method == "GET":
        departmentModel = DepartmentModel.objects.all()
        serializer = DepartmentSerializerGet(departmentModel, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == "POST":
        data = JSONParser().parse(request)
        serializer = DepartmentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        else:
            return JsonResponse(serializer.errors, status=400)

@csrf_exempt
@require_http_methods(["GET", "POST"])
@login_required
def employee_list(request):
    if request.method == "GET":
        employeeModel = EmployeeModel.objects.all()
        serializers = EmployeeSerializerGet(employeeModel, many=True)
        return JsonResponse(serializers.data, safe=False)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializers = EmployeeSerializer(data=data)
        if serializers.is_valid():
            serializers.save()
            return JsonResponse(serializers.data, status=201)
        else:
            return JsonResponse(serializers.errors, status=400)

@csrf_exempt      
@require_http_methods(["GET", "PUT", "DELETE"])
@login_required
def position_detail(request, id):
    positionModel = get_object_or_404(PositionModel, pk=id)

    if request.method == 'GET':
        serializers = PositionSerializer(positionModel)
        return JsonResponse(serializers.data, safe=False)
    
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializers = PositionSerializer(positionModel, data=data)
        if serializers.is_valid():
            serializers.save()
            return JsonResponse(serializers.data, status=201)
        else:
            return JsonResponse(serializers.errors, status=400)
    
    elif request.method == 'DELETE':
        positionModel.delete()
        return HttpResponse(status=204)

@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
@login_required       
def department_detail(request, id):
    departmentModel = get_object_or_404(DepartmentModel, pk=id)
    if request.method == 'GET':
        serializers = DepartmentSerializerGet(departmentModel)
        return JsonResponse(serializers.data, safe=False)
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializers = DepartmentSerializer(departmentModel, data=data)
        if serializers.is_valid():
            serializers.save()
            return JsonResponse(serializers.data, status=201)
        else:
            return JsonResponse(serializers.errors, status=400)
    elif request.method == 'DELETE':
        departmentModel.delete()
        return HttpResponse(status=204)

@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
@login_required
def employee_detail(request, id):
    employeeModel = get_object_or_404(EmployeeModel, pk=id)
    if request.method == 'GET':
        serializers = EmployeeSerializerGet(employeeModel)
        return JsonResponse(serializers.data, safe=False)
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializers = EmployeeSerializer(employeeModel, data=data)
        if serializers.is_valid():
            serializers.save()
            return JsonResponse(serializers.data, status=201)
        else: 
            return JsonResponse(serializers.errors, status=400)
    elif request.method == 'DELETE':
        employeeModel.delete()
        return HttpResponse(status=204)
