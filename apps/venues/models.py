from django.db import models
from apps.shared.models import BaseModel

class Venue(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100)
    capacity = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.name}, {self.city}"