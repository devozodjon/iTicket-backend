from django.db import models

from apps.shared.models import BaseModel
from apps.users.models.user import User


class Organizer(BaseModel):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='organizer',
        null=True,
        blank=True
    )
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    company_name = models.CharField(max_length=255)
    business_license = models.CharField(max_length=100)
    bank_account = models.CharField(max_length=100)
    email = models.EmailField(max_length=255, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.company_name} ({self.first_name} {self.last_name})"

    class Meta:
        verbose_name = 'Organizer'
        verbose_name_plural = 'Organizers'