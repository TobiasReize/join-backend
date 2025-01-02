from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):    # damit wird der Django-User ergänzt! (nicht verändert)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField()

    def __str__(self):
        return self.user.username
