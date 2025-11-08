from .models import *
from .serializers import *
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.
@csrf_exempt
@api_view(["GET", "POST"])
@login_required    
def position_list(request):
    if request.method == "GET":
        positionModel = PositionModel.objects.all()
        serializer = PositionSerializer(positionModel, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        
        serializer = PositionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)

@csrf_exempt
@api_view(["GET", "POST"])
@login_required    
def department_list(request):
    if request.method == "GET":
        departmentModel = DepartmentModel.objects.all()
        serializer = DepartmentSerializerGet(departmentModel, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = DepartmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)

@csrf_exempt
@api_view(["GET", "POST"])
@login_required    
def employee_list(request):
    if request.method == "GET":
        employeeModel = EmployeeModel.objects.all()
        serializers = EmployeeSerializerGet(employeeModel, many=True)
        return Response(serializers.data)
    elif request.method == 'POST':
        
        serializers = EmployeeSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=201)
        else:
            return Response(serializers.errors, status=400)

@csrf_exempt      
@api_view(["GET", "PUT", "DELETE"])
@login_required    
def position_detail(request, id):
    positionModel = get_object_or_404(PositionModel, pk=id)

    if request.method == 'GET':
        serializers = PositionSerializer(positionModel)
        return Response(serializers.data)
    
    elif request.method == 'PUT':
        
        serializers = PositionSerializer(positionModel, data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=201)
        else:
            return Response(serializers.errors, status=400)
    
    elif request.method == 'DELETE':
        positionModel.delete()
        return Response(status=204)

@csrf_exempt
@api_view(["GET", "PUT", "DELETE"])
@login_required       
def department_detail(request, id):
    departmentModel = get_object_or_404(DepartmentModel, pk=id)
    if request.method == 'GET':
        serializers = DepartmentSerializerGet(departmentModel)
        return Response(serializers.data)
    elif request.method == 'PUT':
        
        serializers = DepartmentSerializer(departmentModel, data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=201)
        else:
            return Response(serializers.errors, status=400)
    elif request.method == 'DELETE':
        departmentModel.delete()
        return Response(status=204)

@csrf_exempt
@api_view(["GET", "PUT", "DELETE"])
@login_required    
def employee_detail(request, id):
    employeeModel = get_object_or_404(EmployeeModel, pk=id)
    if request.method == 'GET':
        serializers = EmployeeSerializerGet(employeeModel)
        return Response(serializers.data)
    elif request.method == 'PUT':
        
        serializers = EmployeeSerializer(employeeModel, data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=201)
        else: 
            return Response(serializers.errors, status=400)
    elif request.method == 'DELETE':
        employeeModel.delete()
        return Response(status=204)
