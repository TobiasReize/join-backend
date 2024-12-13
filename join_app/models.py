from django.db import models


class Summary(models.Model):
    to_do = models.IntegerField(null=True)
    in_progress = models.IntegerField(null=True)
    await_feedback = models.IntegerField(null=True)
    done = models.IntegerField(null=True)
    urgent = models.IntegerField(null=True)
    all = models.IntegerField(null=True)


class Contact(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=100)
    checked = models.BooleanField(default=False)
    color = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Task(models.Model):
    column_id = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    contacts = models.ManyToManyField(Contact, related_name='tasks')           # many-to-many: ein Task kann mehrere Kontakte haben und ein Kontakt kann mehreren Tasks zugeordnet sein!
    priority = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Subtask(models.Model):
    status = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='subtasks')   # one-to-many: ein Task kann mehrere Subtasks haben aber ein Subtask gehört nur zu einem bestimmten Task!

    def __str__(self):
        return f"{self.status}: {self.title}"