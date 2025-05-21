from .serializers import RegisterSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny, IsAuthenticated, SAFE_METHODS, BasePermission
from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .serializers import QatagonlarSerializers, QatagonlarDetailSerializers
from .models import QatagonlarClassModel

# Create your views here.


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.owner == request.user


class QatagonlarViewSet(ModelViewSet):
    queryset = QatagonlarClassModel.objects.all()
    lookup_field = 'slug'
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if 'name' in self.request.GET:
            queryset = QatagonlarClassModel.objects.filter(
                Q(full_name__icontains=self.request.GET['name'])
                |
                Q(birth_year__icontains=self.request.GET['name'])
            )
        else:
            queryset = QatagonlarClassModel.objects.all()

        return queryset

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'name',
                openapi.IN_QUERY,
                description="Full name bo'yicha qidirish",
                type=openapi.TYPE_STRING
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.action == 'list':
            return QatagonlarSerializers
        elif self.action == 'retrieve':
            return QatagonlarDetailSerializers
        return QatagonlarDetailSerializers

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated(), IsOwnerOrReadOnly()]


class RegisterView(APIView):
    @swagger_auto_schema(request_body=RegisterSerializer)
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Ro'yxatdan o'tdingiz"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
