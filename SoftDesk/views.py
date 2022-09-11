from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from SoftDesk.models import Project, Contributor, Comment, Issue
from SoftDesk.serializers import UserSerializer, GroupSerializer, \
    ProjectSerializer, IssueSerializer, ContributorSerializer, \
    CommentSerializer
from SoftDesk.permissions import IsOwner, IsContributorOrProjectOwner
from .serializers import RegisterSerializer
from rest_framework import generics


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows projects to be viewed or edited.
    """

    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        return Project.objects.filter(Q(author=self.request.user) |
                                      Q(contributors=self.request.user)).distinct()

    def get_permissions(self):
        if self.request.method in ['PUT', 'DELETE', 'PATCH']:
            return [permissions.IsAuthenticated(), IsOwner()]
        return [permissions.IsAuthenticated()]


class ContributorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users of a project to be viewed or edited.
    """
    serializer_class = ContributorSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        project = Project.objects.get(id=self.kwargs['project_pk'])
        serializer.save(project=project)

    def get_queryset(self):
        pk = self.kwargs['project_pk']
        return Contributor.objects.filter(project__id=pk)

    def get_permissions(self):
        if self.request.method in ['POST', 'DELETE', 'PUT', 'PATCH']:
            return [permissions.IsAuthenticated(), IsOwner()]
        if self.request.method in ['GET', 'LIST']:
            return [permissions.IsAuthenticated(),
                    IsContributorOrProjectOwner()]
        return [permissions.IsAuthenticated()]


class IssueViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users of a project to be viewed or edited.
    """
    serializer_class = IssueSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        project = Project.objects.get(id=self.kwargs['project_pk'])
        serializer.save(author=self.request.user, project=project)

    def get_queryset(self):
        pk = self.kwargs['project_pk']
        return Issue.objects.filter(project__id=pk)

    def get_permissions(self):
        if self.request.method in ['PUT', 'DELETE', 'PATCH']:
            return [permissions.IsAuthenticated(), IsOwner()]
        if self.request.method in ['POST', 'GET', 'LIST']:
            return [permissions.IsAuthenticated(),
                    IsContributorOrProjectOwner()]
        return [permissions.IsAuthenticated()]


class CommentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users of a project to be viewed or edited.
    """
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        issue = Issue.objects.get(id=self.kwargs['issue_pk'])
        serializer.save(author=self.request.user, issue=issue)

    def get_queryset(self):
        pk = self.kwargs['issue_pk']
        return Comment.objects.filter(issue__id=pk)

    def get_permissions(self):
        if self.request.method in ['PUT', 'DELETE', 'PATCH']:
            return [permissions.IsAuthenticated(), IsOwner()]
        if self.request.method in ['POST', 'GET', 'LIST']:
            return [permissions.IsAuthenticated(),
                    IsContributorOrProjectOwner()]
        return [permissions.IsAuthenticated()]


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
