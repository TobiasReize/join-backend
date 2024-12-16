from rest_framework import serializers
from datetime import date

from join_app.models import Summary, Contact, Subtask, Task


class SummarySerializer(serializers.ModelSerializer):
    to_do = serializers.SerializerMethodField()
    in_progress = serializers.SerializerMethodField()
    await_feedback = serializers.SerializerMethodField()
    done = serializers.SerializerMethodField()
    urgent = serializers.SerializerMethodField()
    all = serializers.SerializerMethodField()
    class Meta:
        model = Summary
        fields = '__all__'


    def get_all(self, objects):
        return objects.count()

    def get_to_do(self, objects):
        number_to_do = objects.filter(columnID='ToDo').count()
        return number_to_do
    
    def get_in_progress(self, objects):
        number_in_progress = objects.filter(columnID='InProgress').count()
        return number_in_progress
    
    def get_await_feedback(self, objects):
        number_await_feedback = objects.filter(columnID='AwaitFeedback').count()
        return number_await_feedback
    
    def get_done(self, objects):
        number_done = objects.filter(columnID='Done').count()
        return number_done
    
    def get_urgent(self, objects):
        number_urgent = objects.filter(priority='urgent').count()
        return number_urgent


class ContactSerializer(serializers.ModelSerializer):
    tasks = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='task-detail')
    class Meta:
        model = Contact
        fields = ['firstName', 'lastName', 'mail', 'tel', 'checked', 'color', 'tasks']


class SubtaskSerializer(serializers.ModelSerializer):
    status = serializers.ChoiceField(choices=['open', 'done'], style={'base_template': 'select.html'}, initial='open')
    task = serializers.HyperlinkedRelatedField(read_only=True, view_name='task-detail')
    task_id = serializers.PrimaryKeyRelatedField(queryset=Task.objects.all(), write_only=True, source='task')
    class Meta:
        model = Subtask
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    date = serializers.DateField(initial=date.today)
    columnID = serializers.ChoiceField(choices=['ToDo', 'InProgess', 'AwaitFeedback', 'Done'], style={'base_template': 'select.html'}, initial='ToDo')
    category = serializers.ChoiceField(choices=['Technical Task', 'User Story'], style={'base_template': 'select.html'}, initial='Technical Task')
    priority = serializers.ChoiceField(choices=['low', 'medium', 'urgent'], style={'base_template': 'select.html'}, initial='low')
    contacts = serializers.StringRelatedField(many=True, read_only=True)
    contact_ids = serializers.PrimaryKeyRelatedField(queryset=Contact.objects.all(), many=True, write_only=True, source='contacts')
    subtasks = serializers.StringRelatedField(many=True, read_only=True)
    # subtask_ids = serializers.PrimaryKeyRelatedField(queryset=Subtask.objects.all(), many=True, write_only=True, source='subtasks')

    class Meta:
        model = Task
        fields = ['id', 'columnID', 'category', 'title', 'description', 'date', 'priority', 'contacts', 'contact_ids', 'subtasks']


class TaskListSerializer(serializers.ListSerializer):

    def create(self, validated_data):   # validated_data ist eine Liste mit Dictionaries --> [{...}, {...}, ...] (jedes Dict ist hierbei eine vollständige Task!)
        print("validated_data (TaskListSerializer):", validated_data)
        all_contacts = Contact.objects.all()
        new_tasks = []
        
        for item in validated_data:     # Haupt-For-Schleife zum Behandeln jedes einzelne Task-Objekt
            
            # Priority:
            priority_obj = item.pop('priority')     # ist ein Dictionary: {"low":False,"medium":False,"urgent":True}
            for key in priority_obj.keys():         # Schleife zum Bestimmen der Priorität
                if priority_obj[key]:
                    task_priority = key
                    break
            print("priority is:", task_priority)
            
            # Contacts:
            contacts_list = item.pop('contacts')       # ist eine Liste mit Dictionaries: [{"checked":true,"color":"#6E52FF","firstName":"Charlie","lastName":"Brown","mail":"charlie.brown@example.com","tel":"+49 151 34567890"}, {...}
            task_contacts = []
            for contact_data in contacts_list:                  # Schleife zum Erstellen der einzelnen Kontakte (werden in der task_contacts Liste gespeichert)
                contact = all_contacts.get(firstName=contact_data['firstName'], lastName=contact_data['lastName'], mail=contact_data['mail'], tel=contact_data['tel'], color=contact_data['color'], checked=contact_data['checked'])
                task_contacts.append(contact)
            print("task_contacts:", task_contacts)

            # Subtasks:
            task_subtasks = []        # ist eine Liste mit Subtask-Dictionaries
            if 'taskSubtasks' in item.keys():
                subtasks_list = item.pop('taskSubtasks')
                for subtask_data in subtasks_list:
                    subtask = Subtask(**subtask_data)   # hier wird das neue Subtask-Objekt erzeugt! (aber nicht gespeichert! Dies wird durch die set-Methode mit bulk=False gemacht!)
                    task_subtasks.append(subtask)
            print('task_subtasks:', task_subtasks)

            # Tasks:
            task = Task.objects.create(priority=task_priority, **item)     # ein einzelnes Task-Objekt wird mit den Daten erstellt (und gleich in die Datenbank gespeichert?)
            task.contacts.set(task_contacts)    # die Kontakte dürfen nicht beim Erstellen des Task-Objektes enthalten sein (wegen many-to-many)! Daher wird es nachträglich mit der set() Methode gemacht!
            task.subtasks.set(task_subtasks, bulk=False)    # mit bulk=False werden die neuen Subtask-objekte in der Datenbank gespeichert! (die save-Methode wird ausgeführt!)
            new_tasks.append(task)      # die einzelnen Task-Objekte werden in einer Liste gespeichert!
        return new_tasks


class TaskCreateSerializer(serializers.ModelSerializer):          # bei einem neuen Task, wird zuerst die Task-Instanz (inkl. Kontakte) ohne Subtask erstellt und dann muss im Subtask-Serializer die Subtask-Instanz erstellt und die Task-ID zugewiesen werden!
    date = serializers.DateField(initial=date.today)
    columnID = serializers.ChoiceField(choices=['ToDo', 'InProgess', 'AwaitFeedback', 'Done'], style={'base_template': 'select.html'}, initial='ToDo')
    category = serializers.ChoiceField(choices=['Technical Task', 'User Story'], style={'base_template': 'select.html'}, initial='Technical Task')
    priority = serializers.DictField(child=serializers.BooleanField())
    contacts = ContactSerializer(many=True)     # darf nicht "read_only=True" sein, sonst sind die Daten nicht in "validated_data" vorhanden!
    taskSubtasks = serializers.ListSerializer(required=False, child=serializers.DictField(child=serializers.CharField()))

    class Meta:
        model = Task
        fields = ['id', 'columnID', 'category', 'title', 'description', 'date', 'priority', 'contacts', 'taskSubtasks']
        list_serializer_class = TaskListSerializer
