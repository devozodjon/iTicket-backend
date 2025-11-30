from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils.text import slugify

from apps.users.models.organizer import Organizer
from apps.users.models.user import User
from apps.venues.models import Venue
from apps.shared.models import Media, BaseModel


class Category(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Events(BaseModel):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('cancelled', 'Cancelled'),
    ]

    title = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='events')
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField(blank=True, null=True)

    organizer = models.ForeignKey(
        Organizer, on_delete=models.CASCADE, related_name='organized_events'
    )

    venue = models.ForeignKey(
        Venue, on_delete=models.SET_NULL, null=True, blank=True, related_name='events'
    )

    media_fields = GenericRelation(Media, blank=True, related_name='events')

    participants = models.ManyToManyField(
        User, blank=True, related_name='participating_events'
    )

    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()

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
