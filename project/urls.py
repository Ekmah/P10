from django.contrib import admin
from django.urls import include, path
# from rest_framework import routers
from rest_framework_nested import routers
from SoftDesk import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'projects', views.ProjectViewSet, 'project')


project_sub_routes = routers.NestedSimpleRouter(router,
                                                r'projects', lookup='project')
project_sub_routes.register(r'users',
                            views.ContributorViewSet, basename='contributor')
project_sub_routes.register(r'issues',
                            views.IssueViewSet, basename='issue')


issue_sub_routes = routers.NestedSimpleRouter(project_sub_routes,
                                              r'issues', lookup='issue')
issue_sub_routes.register(r'comments',
                          views.CommentViewSet, basename='comment')
# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('', include(project_sub_routes.urls)),
    path('', include(issue_sub_routes.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
