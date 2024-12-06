from rest_framework import serializers
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
    class Meta:
        model = Contact
        fields = '__all__'


class SubtaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subtask
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    contacts = serializers.StringRelatedField(many=True, read_only=True)
    subtasks = serializers.StringRelatedField(many=True, read_only=True)
    class Meta:
        model = Task
        fields = ['column_id', 'category', 'title', 'description', 'date', 'priority', 'contacts', 'subtasks']
