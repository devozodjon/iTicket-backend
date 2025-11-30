from django.db import models
from apps.events.models import Events
from apps.venues.models import Venue
from apps.shared.models import BaseModel

class SeatSection(BaseModel):
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name='sections')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.venue.name} - {self.name}"

class Seat(BaseModel):
    event = models.ForeignKey(Events, on_delete=models.CASCADE, related_name='seats')
    section = models.ForeignKey(SeatSection, on_delete=models.SET_NULL, null=True, blank=True, related_name='seats')
    row = models.CharField(max_length=10, blank=True, null=True)
    number = models.CharField(max_length=10)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_reserved = models.BooleanField(default=False)

    class Meta:
        unique_together = ('event', 'row', 'number')
        indexes = [
            models.Index(fields=['event', 'section']),
        ]

    def __str__(self):
        section_name = self.section.name if self.section else 'Seat'
        return f"{self.event.title} - {section_name} {self.row}-{self.number}"