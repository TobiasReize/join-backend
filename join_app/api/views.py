from .serializers import SummarySerializer, ContactSerializer, SubtaskSerializer, TaskSerializer, TaskCreateSerializer
from join_app.models import Summary, Contact, Subtask, Task

from rest_framework import viewsets
from rest_framework.response import Response


class SummaryView(viewsets.ViewSet):     # nur GET-Methode
    def retrieve(self, request, pk=None):
        queryset = Task.objects.all()
        serializer = SummarySerializer(queryset)
        summary = Summary(id=1, **serializer.data)  # dadurch, dass die id immer 1 ist, wird immer das selbe Objekt geupdated! (kein neues erzeugt!)
        summary.save()
        return Response(serializer.data)


class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer


class SubtaskViewSet(viewsets.ModelViewSet):
    queryset = Subtask.objects.all()
    serializer_class = SubtaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()   # sind die Daten aus der Datenbank!
    serializer_class = TaskSerializer

    def create(self, request, *args, **kwargs):
        serializer = TaskCreateSerializer(data=request.data, many=True)   # aktuell werden immer alle Tasks hochgeladen! (daher many=True)
        print("serializer (View):", request.data)
        if serializer.is_valid(raise_exception=True):
            print("serializer is valid (View)! serializer.data:", serializer.data)
            Task.objects.all().delete()     # zunächst werden alle Tasks aus der Datenbank gelöscht (um danach wieder alle zu erstellen!)
            serializer.save()               # hier werden alle Task-Objekte erstellt! (durch den Serializer)
        else: print("serializer is not valid!", serializer.data)
        return Response(serializer.data)
