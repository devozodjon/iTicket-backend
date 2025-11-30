from django.db import models
from django.utils.text import slugify
from apps.users.models.user import User
from apps.venues.models import Venue
from apps.shared.models import Media, BaseModel


class Events(BaseModel):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('cancelled', 'Cancelled'),
    ]

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField(blank=True, null=True)

    organizer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='organized_events'
    )

    venue = models.ForeignKey(
        Venue, on_delete=models.SET_NULL, null=True, blank=True, related_name='events'
    )

    media = models.ManyToManyField(
        Media, blank=True, related_name='events'
    )

    participants = models.ManyToManyField(
        User, blank=True, related_name='participating_events'
    )

    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()

    category = models.CharField(max_length=100, blank=True, null=True)
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    tickets_total = models.PositiveIntegerField(default=0)
    tickets_sold = models.PositiveIntegerField(default=0)

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    class Meta:
        ordering = ['-start_datetime']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['start_datetime']),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
