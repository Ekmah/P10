from django.contrib.auth.models import User, Group
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator

from rest_framework import serializers
from SoftDesk.models import Project, Issue, Contributor, Comment


class ContributorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Contributor
        depth = 0
        fields = ['id', 'project_id', 'user_id']
        read_only_fields = ['project_id', 'user_id']


class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    contributors = serializers.PrimaryKeyRelatedField(many=True,
                                                      read_only=True)

    class Meta:
        model = Project
        depth = 0
        fields = ['id', 'author_id', 'contributors', 'title',
                  'description', 'project_type']
        read_only_fields = ['author']


class IssueSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Issue
        depth = 0
        fields = ['id', 'project_id', 'author_id', 'assigned_user_id', 'title',
                  'description', 'tag', 'priority', 'status', 'created_time']
        read_only_fields = ['project_id', 'author_id', 'assigned_user']


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    issue = serializers.ReadOnlyField(source='issue.issue_id')

    class Meta:
        model = Comment
        depth = 0
        fields = ['id', 'issue_id', 'author_id', 'description', 'created_time']
        read_only_fields = ['author_id', 'issue_id']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']


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
