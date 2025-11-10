from .models import *
from .serializers import *
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q


# Create your views here.
@csrf_exempt
@api_view(["GET", "POST"])
@login_required    
def position_list(request):
    if request.method == "GET":
        positionModel = PositionModel.objects.all()
        serializers = PositionSerializer(positionModel, many=True)
        return Response(serializers.data)
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
        serializers = DepartmentSerializerGet(departmentModel, many=True)
        return Response(serializers.data)
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
        if request.GET.get('q'):
            employeeModel = employeeModel.filter(Q(name__icontains = request.GET.get('q')) | 
                                                        Q(position__position_name__icontains = request.GET.get('q')) | 
                                                        Q(department__department_name__icontains = request.GET.get('q')))
        if request.GET.get('sort'):
            if request.GET.get('sort') == 'name':
                employeeModel = employeeModel.order_by('name')
            elif request.GET.get('sort') == 'position':
                employeeModel = employeeModel.order_by('position__position_name')
            elif request.GET.get('sort') == 'department':
                employeeModel = employeeModel.order_by('department__department_name')
        serializers = EmployeeSerializerGet(employeeModel, many=True)
        return Response(serializers.data)
    elif request.method == 'POST':
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)

@csrf_exempt      
@api_view(["GET", "PUT", "DELETE"])
@login_required    
def position_detail(request, id):
    positionModel = get_object_or_404(PositionModel, pk=id)
    if request.method == 'GET':
        serializer = PositionSerializer(positionModel)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = PositionSerializer(positionModel, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)
    elif request.method == 'DELETE':
        positionModel.delete()
        return Response(status=204)

@csrf_exempt
@api_view(["GET", "PUT", "DELETE"])
@login_required       
def department_detail(request, id):
    departmentModel = get_object_or_404(DepartmentModel, pk=id)
    if request.method == 'GET':
        serializer = DepartmentSerializerGet(departmentModel)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = DepartmentSerializer(departmentModel, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)
    elif request.method == 'DELETE':
        departmentModel.delete()
        return Response(status=204)

@csrf_exempt
@api_view(["GET", "PUT", "DELETE"])
@login_required    
def employee_detail(request, id):
    employeeModel = get_object_or_404(EmployeeModel, pk=id)
    if request.method == 'GET':
        serializer = EmployeeSerializerGet(employeeModel)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = EmployeeSerializer(employeeModel, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else: 
            return Response(serializer.errors, status=400)
    elif request.method == 'DELETE':
        employeeModel.delete()
        return Response(status=204)
