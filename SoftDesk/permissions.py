from rest_framework import permissions
from rest_framework import exceptions
from SoftDesk.models import Contributor, Comment, Issue, Project

# determine type of authorisations
# determine place where authorisation checks are wanted
# realize the checks needs & frame
# code.


class IsOwner(permissions.BasePermission):
    """
    Allows access only to authenticated owners.
    """

    def has_permission(self, request, view):
        if 'pk' in view.kwargs:
            obj = view.get_object()
            return self.has_object_permission(request, view, obj)
        else:
            value = False
            if str(type(view)) == \
                    "<class 'SoftDesk.views.ContributorViewSet'>":
                project = Project.objects.get(id=view.kwargs['project_pk'])
                if request.user == project.author:
                    value = True
            return value

    def has_object_permission(self, request, view, obj):
        if obj._meta.object_name == 'Contributor':
            project = Project.objects.get(id=view.kwargs['project_pk'])
            return bool(project.author == request.user)
        value = bool(obj.author == request.user)
        return value


class IsContributorOrProjectOwner(permissions.BasePermission):
    """
    Allows access only to contributors or project owners.
    """

    def has_permission(self, request, view):
        if 'pk' in view.kwargs:
            obj = view.get_object()
            return self.has_object_permission(request, view, obj)
        else:
            value = False
            project = Project.objects.get(id=view.kwargs['project_pk'])
            if request.user in project.contributors.all() or \
                    request.user == project.author:
                value = True
            return value

    def has_object_permission(self, request, view, obj):
        value = False
        project = Project.objects.get(id=view.kwargs['project_pk'])
        try:
            if request.user in project.contributors.all() or \
                    request.user == obj.project.author:
                value = True
        except AttributeError:
            if request.user in project.contributors.all() or \
                    request.user == obj.issue.project.author:
                value = True
        return value
