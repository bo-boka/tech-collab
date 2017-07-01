# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from collab.models import Technology
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    picture = models.ImageField(blank=True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    technologies = models.ManyToManyField(Technology, blank=True)
    bio = models.CharField(max_length=500, blank=True)
    experience = models.CharField(max_length=500, blank=True)
    availability = models.CharField(max_length=500, blank=True)
    # socials = models.

    def __str__(self):
        return unicode(self.user)


# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         UserProfile.objects.create(user=instance)
#
#
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.userprofile.save()

