from rest_framework import viewsets, mixins, status
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from django.db.models import Count, Q, Sum
from django.utils import timezone
from datetime import timedelta
from django.contrib.contenttypes.models import ContentType
from .models import Thread, Comment, Like, KarmaActivity
from .serializers import ThreadSerializer, CommentSerializer, CreateCommentSerializer, KarmaActivitySerializer
from django.db import transaction

@method_decorator(csrf_exempt, name='dispatch')
class ThreadViewSet(viewsets.ModelViewSet):
    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        user = self.request.user
        qs = Thread.objects.annotate(
            comments_count=Count('comments', distinct=True),
            likes_count=Count('likes', distinct=True) # This counts likes on the thread
        ).order_by('-created_at')
        
        # Determine if current user liked the thread
        # This is a bit tricky with annotate across generic relations, but for Thread we can do:
        # Actually Like has a GenericForeignKey. It's harder to annotate is_liked efficiently without subqueries.
        # For prototype simplicity, we might do it in serializer or use a Prefetch object?
        # Let's try to simple annotation if possible, or just accept N+1 for "is_liked" for now, or use Exists subquery.
        
        return qs

    def perform_create(self, serializer):
        user = self.request.user
        if user.is_anonymous:
            # Get or create a default 'Guest' user
            user, _ = User.objects.get_or_create(username='Guest')
        serializer.save(author=user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        
        # Optimized Comment Fetching (Solves N+1)
        # 1. Fetch ALL comments for this thread in one query
        all_comments = Comment.objects.filter(thread=instance).select_related('author').annotate(
            likes_count=Count('likes')
        ).order_by('created_at')

        # 2. Build a look-up dictionary
        comment_map = {c.id: c for c in all_comments}
        
        # 3. Initialize 'prefetched_replies' list for all
        for c in comment_map.values():
            c.prefetched_replies = []

        # 4. Assemble the tree
        root_comments = []
        for c in all_comments:
            if c.parent_id:
                if c.parent_id in comment_map:
                    comment_map[c.parent_id].prefetched_replies.append(c)
            else:
                root_comments.append(c)
        
        # 5. Sort root comments (newest first)
        root_comments.sort(key=lambda x: x.created_at, reverse=True)

        # 6. Serialize the tree
        data['comments'] = CommentSerializer(root_comments, many=True, context={'request': request}).data
        return Response(data)

@method_decorator(csrf_exempt, name='dispatch')
class CommentViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Comment.objects.all()
    serializer_class = CreateCommentSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = self.request.user
        if user.is_anonymous:
            user, _ = User.objects.get_or_create(username='Guest')
        serializer.save(author=user)

@method_decorator(csrf_exempt, name='dispatch')
class LikeViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def create(self, request):
        user = request.user
        if user.is_anonymous:
            user, _ = User.objects.get_or_create(username='Guest')
        content_type_str = request.data.get('content_type')
        object_id = request.data.get('object_id')

        try:
            if content_type_str == 'thread':
                app_label, model = 'feed', 'thread'
            elif content_type_str == 'comment':
                app_label, model = 'feed', 'comment'
            else:
                return Response({'error': 'Invalid content_type'}, status=400)
            
            content_type = ContentType.objects.get(app_label=app_label, model=model)
            
            # Atomic transaction to handle race conditions
            with transaction.atomic():
                # select_for_update not available on sqlite? It is but limited.
                # For sqlite validation, atomic is enough.
                like, created = Like.objects.get_or_create(
                    user=user,
                    content_type=content_type,
                    object_id=object_id
                )
                if not created:
                    like.delete()
                    return Response({'status': 'unliked'})
                
                return Response({'status': 'liked'})
        
        except Exception as e:
            return Response({'error': str(e)}, status=400)

class LeaderboardViewSet(viewsets.ViewSet):
    def list(self, request):
        last_24h = timezone.now() - timedelta(hours=24)
        
        # Aggregate karma
        leaderboard = KarmaActivity.objects.filter(
            created_at__gte=last_24h
        ).values('user__username').annotate(
            total_karma=Sum('amount')
        ).order_by('-total_karma')[:10]
        
        return Response(leaderboard)
