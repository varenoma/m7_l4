from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import QatagonlarViewSet, RegisterView


router = DefaultRouter()

router.register(r'lists', QatagonlarViewSet, basename='list')

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('', include(router.urls))
]
