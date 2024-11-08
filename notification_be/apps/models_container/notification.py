from django.db import models
import uuid
from notification_be.apps.enum_container import NotificationType
from  notification_be.apps.models_container import User
from django.utils import timezone

class Notification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User,default=uuid.uuid4, related_name='notification_user', on_delete=models.CASCADE)
    object_type_id = models.UUIDField(default=uuid.uuid4, editable=False)
    notification_type = models.CharField(
        max_length=20,
        choices=[(tag.value, tag.value) for tag in NotificationType]
    )
    recipient = models.ForeignKey(User, default=uuid.uuid4, related_name='notification_recipient', on_delete=models.CASCADE)
    data = models.JSONField(default=dict)
    unread = models.IntegerField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    objects = models.Manager()

    def __str__(self):
        return f"Notification to user {self.user} about {self.notification_type}"