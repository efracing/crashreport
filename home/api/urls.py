from django.urls import include, path
from rest_framework import routers

from home.api.views import BuildPdfAPIView


router = routers.DefaultRouter()

urlpatterns = [
    path(
        'crash/report/',
        BuildPdfAPIView.as_view(),
        name='crash-report',
    ),
] + router.urls
