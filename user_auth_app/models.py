from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):    # damit wird der Django-User ergänzt! (nicht verändert)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
