from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    contributors = models.ManyToManyField(User, through='Contributor',
                                          related_name='contributors')
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048, blank=True)
    project_type = models.CharField(max_length=32)


class Contributor(models.Model):
    permissions = (
        ('', ''),
        ('', ''),
    )
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    permission = models.CharField(max_length=20, choices=permissions)
    role = models.CharField(max_length=64)


class Issue(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    assigned_user = models.ForeignKey(User, on_delete=models.CASCADE,
                                      related_name="assigned_user")
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048, blank=True)
    tag = models.CharField(max_length=16)
    priority = models.CharField(max_length=16)
    created_time = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(max_length=2048, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)