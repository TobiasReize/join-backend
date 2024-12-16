from django.db import models


class Summary(models.Model):
    to_do = models.IntegerField(null=True)
    in_progress = models.IntegerField(null=True)
    await_feedback = models.IntegerField(null=True)
    done = models.IntegerField(null=True)
    urgent = models.IntegerField(null=True)
    all = models.IntegerField(null=True)


class Contact(models.Model):
    firstName = models.CharField(max_length=100, db_column='first_name')   # firstName
    lastName = models.CharField(max_length=100, db_column='last_name')    # lastName
    mail = models.EmailField(db_column='email')                     # mail
    tel = models.CharField(max_length=100, db_column='phone')        # tel
    checked = models.BooleanField(default=False)
    color = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.firstName} {self.lastName}"


class Task(models.Model):
    columnID = models.CharField(max_length=100, db_column='column_id')    # columnID
    category = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    contacts = models.ManyToManyField(Contact, related_name='tasks')           # many-to-many: ein Task kann mehrere Kontakte haben und ein Kontakt kann mehreren Tasks zugeordnet sein!
    priority = models.CharField(max_length=100)     # priorities (& DictField oder JSONField???)

    def __str__(self):
        return self.title


class Subtask(models.Model):
    status = models.CharField(max_length=100)
    subtaskTitle = models.CharField(max_length=100, db_column='title')        # subtaskTitle
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='subtasks')   # one-to-many: ein Task kann mehrere Subtasks haben aber ein Subtask gehört nur zu einem bestimmten Task!

    def __str__(self):
        return f"{self.status}: {self.subtaskTitle}"