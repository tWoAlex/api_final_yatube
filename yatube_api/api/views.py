from django.shortcuts import get_object_or_404
from rest_framework import viewsets, filters, generics
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)

from posts.models import Group, Post, Follow
from .serializers import (GroupSerializer, PostSerializer,
                          CommentSerializer, FollowSerializer)
from .permissions import OwnerOrReadOnly


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    permission_classes = (OwnerOrReadOnly, IsAuthenticatedOrReadOnly)
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (OwnerOrReadOnly, IsAuthenticatedOrReadOnly)

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        post = get_object_or_404(Post, pk=post_id)
        new_queryset = post.comments.all()
        return new_queryset

    def perform_create(self, serializer):
        post_id = self.kwargs['post_id']
        post = get_object_or_404(Post, pk=post_id)
        serializer.save(author=self.request.user, post=post)


class FollowViewSet(generics.ListCreateAPIView, viewsets.GenericViewSet):
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated,)

    filter_backends = (filters.SearchFilter,)
    search_fields = ('user__username', 'following__username')

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
