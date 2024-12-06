from django.urls import path, include
from rest_framework import routers

from .views import SummaryView, ContactViewSet, SubtaskViewSet, TaskViewSet


router = routers.SimpleRouter()
router.register(r'contacts', ContactViewSet)
router.register(r'subtasks', SubtaskViewSet)
router.register(r'tasks', TaskViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('summary/', SummaryView.as_view())
]