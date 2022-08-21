from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from SoftDesk.models import Project, Contributor, Comment, Issue
from SoftDesk.serializers import UserSerializer, GroupSerializer, \
    ProjectSerializer, IssueSerializer, ContributorSerializer, \
    CommentSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows projects to be viewed or edited.
    """

    # queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Project.objects.filter(author=self.request.user)


class ContributorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users of a project to be viewed or edited.
    """
    serializer_class = ContributorSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        pk = self.kwargs['project_pk']
        return Contributor.objects.filter(project__id=pk)


class IssueViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users of a project to be viewed or edited.
    """
    serializer_class = IssueSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        pk = self.kwargs['project_pk']
        return Issue.objects.filter(project__id=pk)


class CommentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users of a project to be viewed or edited.
    """
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        pk = self.kwargs['issue_pk']
        return Comment.objects.filter(issue__id=pk)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]
