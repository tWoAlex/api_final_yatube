from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

from posts.models import Group, Post, Comment, Follow, User


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ('id', 'pub_date')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username')

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('id', 'post', 'created')


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True, slug_field='username')
    following = SlugRelatedField(
        read_only=True, slug_field='username')

    class Meta:
        model = Follow
        fields = ('user', 'following')

    def validate(self, attrs):
        data = self.initial_data
        following = data.get('following', None)
        if not following:
            raise serializers.ValidationError(
                '"following" - обязательное поле'
            )
        user = self.context['request'].user
        if following == user.username:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя'
            )
        if not User.objects.filter(username=following).exists():
            raise serializers.ValidationError(
                'Такого автора не существует'
            )
        following = User.objects.get(username=following)
        return {'following': following}

    def create(self, validated_data):
        found = Follow.objects.filter(
            user=self.context['request'].user,
            following=validated_data['following']
        )
        found = found.exists()
        if found:
            raise serializers.ValidationError(
                'Вы уже подписаны на данного автора')

        follow = Follow.objects.create(**validated_data)
        return follow
