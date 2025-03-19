from .models import *
from rest_framework.generics import ListAPIView,CreateAPIView,RetrieveUpdateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import *
from .permissions import HasRolePermission
from rest_framework.response import Response
from rest_framework import status
# Create your views here.
class VehicleListView(ListAPIView):
    # permission_classes = [HasRolePermission]
    # required_permission = 'can_read_vehicles'
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer

class VehicleCreateView(CreateAPIView):
    # permission_classes = [HasRolePermission]
    # required_permission = 'can_create_vehicles'
    # queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer

class VehicleUpdateView(RetrieveUpdateDestroyAPIView):
    lookup_field = 'slug'
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'msg':'Data Updated','data':serializer.data}, status=status.HTTP_200_OK)