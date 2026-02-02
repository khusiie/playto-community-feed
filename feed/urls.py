from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ThreadViewSet, CommentViewSet, LikeViewSet, LeaderboardViewSet

router = DefaultRouter()
router.register(r'threads', ThreadViewSet, basename='thread')
router.register(r'comments', CommentViewSet, basename='comment')
router.register(r'likes', LikeViewSet, basename='like')
router.register(r'leaderboard', LeaderboardViewSet, basename='leaderboard')

urlpatterns = [
    path('', include(router.urls)),
]
