from rest_framework import serializers
from django.contrib.auth.models import User
from django.db.models import Count
from .models import Thread, Comment, Like, KarmaActivity
from django.contrib.contenttypes.models import ContentType

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    replies = serializers.SerializerMethodField()
    likes_count = serializers.IntegerField(read_only=True)
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'content', 'author', 'created_at', 'replies', 'likes_count', 'is_liked']

    def get_is_liked(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return obj.likes.filter(user=user).exists()
        return False

    def get_replies(self, obj):
        if hasattr(obj, 'prefetched_replies'):
             return CommentSerializer(obj.prefetched_replies, many=True, context=self.context).data
        return CommentSerializer(obj.replies.all(), many=True, context=self.context).data

class ThreadSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    comments_count = serializers.IntegerField(read_only=True)
    likes_count = serializers.IntegerField(read_only=True)
    is_liked = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Thread
        fields = ['id', 'title', 'content', 'author', 'created_at', 'comments_count', 'likes_count', 'is_liked', 'comments']

    def get_is_liked(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return obj.likes.filter(user=user).exists()
        return False

    def get_comments(self, obj):
        # Return empty list if thread hasn't been saved yet (no ID)
        if not obj.pk:
            return []
            
        # For list view, fetch root-level comments (without nested replies for performance)
        if hasattr(obj, 'root_comments_cache'):
             return CommentSerializer(obj.root_comments_cache, many=True, context=self.context).data
             
        # Fallback: Fetch root comments directly
        root_comments = list(obj.comments.filter(parent__isnull=True).select_related('author').annotate(
            likes_count=Count('likes')
        ).order_by('-created_at'))
        
        # Set prefetched_replies to empty list to prevent recursive fetching in list view
        for comment in root_comments:
            comment.prefetched_replies = []
        
        return CommentSerializer(root_comments, many=True, context=self.context).data 

class CreateCommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = ['id', 'content', 'thread', 'parent', 'author', 'created_at']
        read_only_fields = ['id', 'author', 'created_at']
        
class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'user', 'created_at']

class KarmaActivitySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = KarmaActivity
        fields = ['user', 'amount', 'description', 'created_at']
