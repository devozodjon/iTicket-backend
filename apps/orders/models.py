# from django.db import models
# from apps.shared.models import BaseModel
# from apps.users.models.user import User
# from apps.events.models import Events
# from apps.seats.models import Seat
#
# class Order(BaseModel):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
#     event = models.ForeignKey(Events, on_delete=models.CASCADE, related_name='orders')
#     seats = models.ManyToManyField(Seat, related_name='orders')
#     total_price = models.DecimalField(max_digits=12, decimal_places=2)
#     is_paid = models.BooleanField(default=False)
#
#     class Meta:
#         ordering = ['-created_at']
#
#     def __str__(self):
#         return f"Order #{self.id} by {self.user.email or self.user.username} for {self.event.title}"
#
# class Ticket(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='tickets')
#     seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
#     issued_at = models.DateTimeField(auto_now_add=True)
#     qr_code = models.CharField(max_length=255, blank=True, null=True)
#
#     class Meta:
#         unique_together = ('order', 'seat')
#
#     def __str__(self):
#         return f"Ticket {self.id} — {self.order.user.email or self.order.user.username} — {self.seat}"
