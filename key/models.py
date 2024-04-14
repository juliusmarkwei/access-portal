from django.db import models
from django.contrib.auth import get_user_model
import uuid
from django.utils import timezone

User = get_user_model()


class AccessKey(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("active", "Active"),
        ("expired", "Expired"),
        ("revoked", "Revoked"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    key = models.CharField(max_length=255, unique=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    procurement_date = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Access Key"
        verbose_name_plural = "Access Keys"

    def __str__(self):
        return str(self.key)[:10]

    def is_active(self):
        return self.status == "active" and self.expires_at > timezone.now()

    def is_expired(self):
        return self.status == "expired" and self.expires_at < timezone.now()

    def is_revoked(self):
        return self.status == "revoked"

    def deactivate(self):
        self.status = "expired"
        self.save()

    def revoke(self):
        self.status = "revoked"
        self.save()
