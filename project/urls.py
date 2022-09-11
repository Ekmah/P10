from django.contrib import admin
from django.urls import include, path
# from rest_framework import routers
from rest_framework_nested import routers
from SoftDesk import views
from rest_framework import urls
router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

project_router = routers.DefaultRouter()
project_router.register(r'projects', views.ProjectViewSet, 'project')


contributor_router = routers.NestedSimpleRouter(project_router,
                                                r'projects', lookup='project')
contributor_router.register(r'users',
                            views.ContributorViewSet, basename='contributor')


issue_router = routers.NestedSimpleRouter(project_router,
                                          r'projects', lookup='project')
issue_router.register(r'issues', views.IssueViewSet, basename='issue')


comment_router = routers.NestedSimpleRouter(issue_router,
                                            r'issues', lookup='issue')
comment_router.register(r'comments', views.CommentViewSet, basename='comment')
# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('', include(project_router.urls)),
    path('', include(contributor_router.urls)),
    path('', include(issue_router.urls)),
    path('', include(comment_router.urls)),
    path('signup/', views.RegisterView.as_view(), name='auth_register'),
    path('', include('rest_framework.urls', namespace='rest_framework'))
]
