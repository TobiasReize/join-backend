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


class SubtaskSerializer(serializers.ModelSerializer):
    status = serializers.ChoiceField(choices=['open', 'done'], style={'base_template': 'select.html'}, initial='open')
    # task = serializers.HyperlinkedRelatedField(read_only=True, view_name='task-detail')
    # task_id = serializers.PrimaryKeyRelatedField(queryset=Task.objects.all(), write_only=True, source='task')
    class Meta:
        model = Subtask
        fields = '__all__'


class ContactSerializer(serializers.ModelSerializer):
    tasks = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='task-detail')
    class Meta:
        model = Contact
        fields = ['id', 'firstName', 'lastName', 'mail', 'tel', 'checked', 'color', 'tasks']


class TaskSerializer(serializers.ModelSerializer):
    date = serializers.DateField(initial=date.today)
    columnID = serializers.ChoiceField(choices=['ToDo', 'InProgress', 'AwaitFeedback', 'Done'], style={'base_template': 'select.html'}, initial='ToDo')
    category = serializers.ChoiceField(choices=['Technical Task', 'User Story'], style={'base_template': 'select.html'}, initial='Technical Task')
    priority = serializers.ChoiceField(choices=['low', 'medium', 'urgent'], style={'base_template': 'select.html'}, initial='low')
    contacts = serializers.StringRelatedField(many=True, read_only=True)
    contact_ids = serializers.PrimaryKeyRelatedField(queryset=Contact.objects.all(), many=True, write_only=True, source='contacts')
    subtasks = SubtaskSerializer(many=True)

    class Meta:
        model = Task
        fields = ['id', 'columnID', 'category', 'title', 'description', 'date', 'priority', 'contacts', 'contact_ids', 'subtasks']


    def create(self, validated_data):
        task_contacts = validated_data.pop('contacts') 
        subtasks_list = validated_data.pop('subtasks')
        task_subtasks = [Subtask(**item) for item in subtasks_list]
        task = Task.objects.create(**validated_data)
        task.contacts.set(task_contacts)
        task.subtasks.set(task_subtasks, bulk=False)    # mit bulk=False werden die neuen Subtask-Objekte in der Datenbank gespeichert! (die save-Methode wird ausgeführt!)
        return task
    

    def update(self, instance, validated_data):
        print('validated_data (TaskSerializer):', validated_data)
        
        instance.columnID = validated_data.get('columnID', instance.columnID)
        instance.category = validated_data.get('category', instance.category)
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.date = validated_data.get('date', instance.date)
        instance.priority = validated_data.get('priority', instance.priority)
        
        # Update contacts if provided
        if 'contacts' in validated_data:
            contact_ids = validated_data.pop('contacts')
            instance.contacts.set(contact_ids)

        # Update subtasks if provided
        if 'subtasks' in validated_data:
            subtasks_data = validated_data.pop('subtasks')
            existing_subtasks = list(instance.subtasks.all())
        
        # Iterate through validated_data and existing_subtasks to update or create
        for i, subtask_data in enumerate(subtasks_data):
            if i < len(existing_subtasks):
                # Update existing subtask
                subtask_instance = existing_subtasks[i]
                subtask_instance.subtaskTitle = subtask_data.get('subtaskTitle', subtask_instance.subtaskTitle)
                subtask_instance.status = subtask_data.get('status', subtask_instance.status)
                subtask_instance.save()
            else:
                # Create new subtask
                Subtask.objects.create(
                    task=instance,
                    subtaskTitle=subtask_data.get('subtaskTitle'),
                    status=subtask_data.get('status')
                )

        # Remove any remaining existing subtasks if there are more than in the input data
        if len(subtasks_data) < len(existing_subtasks):
            for subtask_to_delete in existing_subtasks[len(subtasks_data):]:
                subtask_to_delete.delete()

        instance.save()
        return instance
