from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from .models import Like

User = get_user_model()


class LikeServices:
    """
    Service for manage likes.
    """
    def __init__(self, obj, user):
        self.obj = obj
        self.user = user

    def add_like(self):
        """
        Add like to `obj`.
        """
        obj_type = ContentType.objects.get_for_model(self.obj)
        like, is_created = Like.objects.get_or_create(
            content_type=obj_type, object_id=self.obj.id, user=self.user)
        return like

    def remove_like(self):
        """
        Remove like to `obj`.
        """
        obj_type = ContentType.objects.get_for_model(self.obj)
        Like.objects.filter(
            content_type=obj_type, object_id=self.obj.id, user=self.user
        ).delete()

    def is_fan(self) -> bool:
        """
        Check `user` like to `obj`.
        """
        if not self.user.is_authenticated:
            return False
        obj_type = ContentType.objects.get_for_model(self.obj)
        likes = Like.objects.filter(
            content_type=obj_type, object_id=self.obj.id, user=self.user)
        return likes.exists()
