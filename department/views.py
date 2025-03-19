from django.shortcuts import render
from .models import Department
from rest_framework.views import APIView
from .serializers import *
from .permissions import HasRolePermission
from rest_framework.response import Response
from rest_framework import status
# Create your views here.

class DepartmentRegistrationView(APIView):
    permission_classes = [HasRolePermission]
    serializer_class = DepartmentSerializer
    required_permission = 'can_create_department'
    
    def post(self, request):
        serializer = DepartmentSerializer(data=request.data)
        if serializer.is_valid():
            department = serializer.save()
            return Response({
                'status': 'success',
                'message': 'Department created successfully.',
                'data': DepartmentSerializer(department).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetDepartmentView(APIView):
    permission_classes = [HasRolePermission]
    serializer_class = DepartmentSerializer
    required_permission = 'can_read_department'

    def get(self, request, pk=None):
        department = Department.objects.all()
        if department.exists():
            serializer = DepartmentSerializer(department, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"msg": "No department found."}, status=status.HTTP_404_NOT_FOUND)

class UpdateDepartmentView(APIView):
    permission_classes = [HasRolePermission]
    serializer_class = DepartmentSerializer
    required_permission = 'can_update_department'

    def get(self, request, pk=None):
        if pk is not None:
            department = Department.objects.filter(pk=pk)
            if department.exists():
                serializer = DepartmentSerializer(department, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({"msg": "Department not found."}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, pk=None, format=None):
        department_to_update = Department.objects.filter(pk=pk).first()
        if not department_to_update:
            return Response({"msg": "Department not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = DepartmentSerializer(department_to_update, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Department successfully updated!'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
