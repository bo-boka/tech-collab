# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from datetime import datetime
# from django.utils import timezone


class Technology(models.Model):
    name = models.CharField(unique=True, max_length=50)

    def __str__(self):
        return self.name


class Project(models.Model):
    title = models.CharField(max_length=500)
    founder = models.ForeignKey(User, on_delete=models.CASCADE)
    # date = models.DateTimeField("Date", default=timezone.now())
    date = models.DateTimeField("Date", default=datetime.now())
    description = models.CharField(blank=True, max_length=1000)
    technologies = models.ManyToManyField(Technology)
    archived = models.BooleanField(default=False)
    matches = models.ManyToManyField(User, through='Match', related_name='matches')
    collaborators = models.ManyToManyField(User, through='Collab', related_name='collaborators')

    def get_absolute_url(self):
        return reverse('collab:project', kwargs={'pk': self.pk})

    def __str__(self):
        return "" + self.title + ' - ' + unicode(self.founder)


class Collab(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return unicode(self.user)


class CollabInline(admin.TabularInline):
    model = Collab
    extra = 1


class Match(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return unicode(self.user)


class MatchInline(admin.TabularInline):
    model = Match
    extra = 1
