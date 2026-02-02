from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Like, KarmaActivity

@receiver(post_save, sender=Like)
def add_karma_on_like(sender, instance, created, **kwargs):
    if created:
        # Get the author of the content that was liked
        content_object = instance.content_object
        if hasattr(content_object, 'author'):
            author = content_object.author
            # Determine karma amount based on content type
            amount = 1 # Default for Comment
            if str(content_object._meta) == 'feed.thread':
                 amount = 5
            
            KarmaActivity.objects.create(
                user=author,
                amount=amount,
                description=f"Received a like on {content_object}"
            )
