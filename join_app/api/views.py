from .serializers import SummarySerializer, ContactSerializer, SubtaskSerializer, TaskSerializer
from join_app.models import Summary, Contact, Subtask, Task

from rest_framework import viewsets
from rest_framework import generics


class SummaryView(generics.RetrieveAPIView):     # nur GET-Methode (für ein einzelnes Objekt)
    queryset = Task.objects.all()
    serializer_class = SummarySerializer


class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer


class SubtaskViewSet(viewsets.ModelViewSet):
    queryset = Subtask.objects.all()
    serializer_class = SubtaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer