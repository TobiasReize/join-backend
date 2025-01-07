from django.db import models


class Summary(models.Model):
    to_do = models.IntegerField(null=True)
    in_progress = models.IntegerField(null=True)
    await_feedback = models.IntegerField(null=True)
    done = models.IntegerField(null=True)
    urgent = models.IntegerField(null=True)
    all = models.IntegerField(null=True)


class Contact(models.Model):
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100, blank=True, null=True)
    mail = models.EmailField()
    tel = models.CharField(max_length=100)
    checked = models.BooleanField(default=False)
    color = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.firstName} {self.lastName}"


class Task(models.Model):
    columnID = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    date = models.DateField()
    contacts = models.ManyToManyField(Contact, related_name='tasks')
    priority = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Subtask(models.Model):
    status = models.CharField(max_length=100)
    subtaskTitle = models.CharField(max_length=100)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='subtasks')

    def __str__(self):
        return f"{self.status}: {self.subtaskTitle}"