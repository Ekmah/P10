from django.urls import include, path
from rest_framework_nested import routers
from rest_framework_simplejwt import views as jwt_views
from SoftDesk import views

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
    path('drf', include('rest_framework.urls', namespace='rest_framework')),
    path('login/', jwt_views.TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('login/refresh/', jwt_views.TokenRefreshView.as_view(),
         name='token_refresh'),
]
