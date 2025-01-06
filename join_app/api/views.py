from .serializers import SummarySerializer, ContactSerializer, SubtaskSerializer, TaskSerializer
from join_app.models import Summary, Contact, Subtask, Task

from rest_framework import viewsets
from rest_framework.response import Response


class SummaryView(viewsets.ViewSet):
    def retrieve(self, request, pk=None):
        queryset = Task.objects.all()
        serializer = SummarySerializer(queryset)
        summary = Summary(id=1, **serializer.data)
        summary.save()
        return Response(serializer.data)


class SubtaskViewSet(viewsets.ModelViewSet):
    queryset = Subtask.objects.all()
    serializer_class = SubtaskSerializer


class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
