from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    p_type = (
        ('BE', 'back-end'),
        ('FE', 'front-end'),
        ('iOS', 'iOS'),
        ('AD', 'android'),

    )

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    contributors = models.ManyToManyField(User, through='Contributor',
                                          related_name='contributors')
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048, blank=True)
    project_type = models.CharField(max_length=32, choices=p_type)


class Contributor(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['project', 'user'],
                                    name='unique contributor')
                       ]


class Issue(models.Model):
    priority_type = (
        ('W', 'WEAK'),
        ('M', 'MEDIUM'),
        ('H', 'HIGH'),
    )
    tags = (
        ('B', 'BUG'),
        ('U', 'UPGRADE'),
        ('T', 'TASK'),
    )
    state = (
        ('TD', 'TO_DO'),
        ('IP', 'IN_PROGRESS'),
        ('C', 'COMPLETED'),
    )

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    assigned_user = models.ForeignKey(User, on_delete=models.CASCADE,
                                      related_name="assigned_user")
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048, blank=True)
    tag = models.CharField(max_length=16,
                           choices=tags,
                           default=tags[0][0])
    priority = models.CharField(max_length=16,
                                choices=priority_type,
                                default=priority_type[0][0])
    status = models.CharField(max_length=16,
                              choices=state,
                              default=state[0][0])
    created_time = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(max_length=2048, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
