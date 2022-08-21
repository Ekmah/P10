from django.contrib.auth.models import User, Group
from rest_framework import serializers
from SoftDesk.models import Project, Issue, Contributor, Comment


class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Project
        depth = 0
        fields = ['id', 'url', 'author', 'contributors', 'title',
                  'description', 'project_type']


class ContributorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Contributor
        depth = 0
        fields = ['id', 'project', 'user', 'permission', 'role']


class IssueSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Issue
        depth = 0
        fields = ['id', 'project', 'author', 'assigned_user', 'title',
                  'description', 'tag', 'priority', 'created_time']


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Comment
        depth = 0
        fields = ['id', 'issue', 'author', 'description', 'created_time']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']
