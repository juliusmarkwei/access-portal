from django.db import models
from django.contrib.auth import get_user_model
import uuid
from django.utils import timezone
from django.core.validators import MaxValueValidator
from django.utils.translation import gettext_lazy as _


User = get_user_model()


class AccessKey(models.Model):
    STATUS_CHOICES = [
        ("inactive", "Inactive"),
        ("active", "Active"),
        ("expired", "Expired"),
        ("revoked", "Revoked"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    key = models.CharField(max_length=255, unique=True)
    key_tag = models.CharField(max_length=255, unique=True)
    validity_duration_days = models.IntegerField(
        _("Validity in days"),
        default=30,
        validators=[MaxValueValidator(365)],
        help_text="Validity duration in days",
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="inactive")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    procurement_date = models.DateTimeField(null=True, blank=True)
    expiry_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Access Key"
        verbose_name_plural = "Access Keys"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{str(self.owner)}: KEY - {str(self.key_tag)}"

    def is_active(self):
        return self.status == "active"

    def is_expired(self):
        return self.expiry_date > timezone.now()
