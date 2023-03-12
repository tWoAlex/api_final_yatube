from rest_framework import serializers
from rest_framework.relations import SlugRelatedField, StringRelatedField


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


class UsernameToNameField(serializers.Field):
    def to_representation(self, value):
        return str(value)

    def to_internal_value(self, data):
        if self.context['request'].user.username == data:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя')
        if not User.objects.filter(username=data).exists():
            raise serializers.ValidationError(
                'Такого автора не существует')
        return User.objects.get(username=data)


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True, slug_field='username')
    following = UsernameToNameField()

    class Meta:
        model = Follow
        fields = ('user', 'following')

    def create(self, validated_data):
        # follow, status = Follow.objects.get_or_create(**validated_data)
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
