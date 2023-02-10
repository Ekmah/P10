from django.contrib.auth.models import User, Group
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator

from rest_framework import serializers
from SoftDesk.models import Project, Issue, Contributor, Comment


class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Project
        depth = 0
        fields = ['id', 'url', 'author', 'contributors', 'title',
                  'description', 'project_type']
        read_only_fields = ['author']


class ContributorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Contributor
        depth = 0
        fields = ['id', 'project', 'user']
        read_only_fields = ['project', 'user']


class IssueSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Issue
        depth = 0
        fields = ['id', 'project', 'author', 'assigned_user', 'title',
                  'description', 'tag', 'priority', 'status', 'created_time']
        read_only_fields = ['project', 'author', 'assigned_user']


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    issue = serializers.ReadOnlyField(source='issue.issue_id')

    class Meta:
        model = Comment
        depth = 0
        fields = ['id', 'issue', 'author', 'description', 'created_time']
        read_only_fields = ['author', 'issue']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(write_only=True, required=True,
                                     validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name',
                  'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user
