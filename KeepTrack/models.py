from __future__ import unicode_literals
from django.contrib.auth.models import User

from django.db import models


class KeepTrackUser(models.Model):
    premium = models.BooleanField(default=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Event(models.Model):
    name = models.CharField(max_length=512)
    description = models.CharField(max_length=512)
    date = models.DateTimeField()
    status = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name + " | " + str(self.date)



class Allocation(models.Model):
    user = models.ForeignKey(User)
    event = models.ForeignKey(Event)
    attended = models.BooleanField(default=False)
