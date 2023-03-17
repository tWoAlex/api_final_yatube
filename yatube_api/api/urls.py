from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import GroupViewSet, PostViewSet, CommentViewSet, FollowViewSet

app_name = 'api'

v1_router = DefaultRouter()
v1_router.register('groups', GroupViewSet)
v1_router.register('posts', PostViewSet)
v1_router.register(r'posts/(?P<post_id>[^/.]+)/comments', CommentViewSet,
                   basename='comments')
v1_router.register('follow', FollowViewSet, basename='follows')

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/', include('djoser.urls.jwt'))
]
