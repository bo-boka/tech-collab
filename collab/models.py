# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


class Technology(models.Model):
    name = models.CharField(unique=True, max_length=50)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    phone = models.IntegerField(default=0)
    picture = models.ImageField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    technologies = models.ManyToManyField(Technology)
    bio = models.CharField(max_length=500, blank=True)
    experience = models.CharField(max_length=500, blank=True)
    availability = models.CharField(max_length=500, blank=True)


class Project(models.Model):
    title = models.CharField(max_length=500)
    founder = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField("Date", default=datetime.now())
    description = models.CharField(blank=True, max_length=1000)
    technologies = models.ManyToManyField(Technology)
    archived = models.BooleanField(default=False)

    def __str__(self):
        return self.title + ' - ' + self.founder


class Platform(models.Model):
    name = models.CharField(max_length=20)


class Social(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    platform = models.ForeignKey(Platform)
    url = models.URLField()

    def __str__(self):
        return self.platform + ': ' + self.url


class Request(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipient')

    def __str__(self):
        return 'From: ' + self.sender + ' | ' + self.project


class Collab(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return self.user


class Match(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return self.user
