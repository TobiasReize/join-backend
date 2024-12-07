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
    
    def get_all(self, obj):
        return obj.tasks.count()
    
    def get_to_do(self, obj):
        return obj.tasks.filter(column_id='ToDo').count()
    
    def get_in_progress(self, obj):
        return obj.tasks.filter(column_id='InProgess').count()
    
    def get_await_feedback(self, obj):
        return obj.tasks.filter(column_id='AwaitFeedback').count()
    
    def get_done(self, obj):
        return obj.tasks.filter(column_id='Done').count()
    
    def get_urgent(self, obj):
        return obj.tasks.filter(priority='urgent').count()


class ContactSerializer(serializers.ModelSerializer):
    tasks = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='task-detail')
    class Meta:
        model = Contact
        fields = ['first_name', 'last_name', 'email', 'phone', 'checked', 'color', 'tasks']


class SubtaskSerializer(serializers.ModelSerializer):
    status = serializers.ChoiceField(choices=['open', 'done'], style={'base_template': 'select.html'}, initial='open')
    task = serializers.HyperlinkedRelatedField(read_only=True, view_name='task-detail')
    task_id = serializers.PrimaryKeyRelatedField(queryset=Task.objects.all(), write_only=True, source='task')
    class Meta:
        model = Subtask
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    date = serializers.DateField(initial=date.today)
    column_id = serializers.ChoiceField(choices=['ToDo', 'InProgess', 'AwaitFeedback', 'Done'], style={'base_template': 'select.html'}, initial='ToDo')
    category = serializers.ChoiceField(choices=['Technical Task', 'User Story'], style={'base_template': 'select.html'}, initial='Technical Task')
    priority = serializers.ChoiceField(choices=['low', 'medium', 'urgent'], style={'base_template': 'select.html'}, initial='low')
    contacts = serializers.StringRelatedField(many=True, read_only=True)
    contact_ids = serializers.PrimaryKeyRelatedField(queryset=Contact.objects.all(), many=True, write_only=True, source='contacts')
    subtasks = serializers.StringRelatedField(many=True, read_only=True)
    class Meta:
        model = Task
        fields = ['id', 'column_id', 'category', 'title', 'description', 'date', 'priority', 'contacts', 'contact_ids', 'subtasks']
