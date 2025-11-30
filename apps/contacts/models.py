# from django.db import models
# from apps.shared.models import BaseModel
#
#
# class Contact(BaseModel):
#     company_name = models.CharField(max_length=255, default="iTicket")
#
#     phone = models.CharField(max_length=50, blank=True, null=True)
#     phone_2 = models.CharField(max_length=50, blank=True, null=True)
#
#     email = models.EmailField(blank=True, null=True)
#     support_email = models.EmailField(blank=True, null=True)
#
#     address = models.TextField(blank=True, null=True)
#     work_hours = models.CharField(max_length=255, blank=True, null=True)
#
#     telegram = models.URLField(blank=True, null=True)
#     instagram = models.URLField(blank=True, null=True)
#     facebook = models.URLField(blank=True, null=True)
#     youtube = models.URLField(blank=True, null=True)
#
#     terms_url = models.URLField(blank=True, null=True)
#     privacy_policy_url = models.URLField(blank=True, null=True)
#
#     google_map = models.URLField(blank=True, null=True)
#
#     class Meta:
#         verbose_name = "Contact Info"
#         verbose_name_plural = "Contact Information"
#
#     def __str__(self):
#         return f"{self.company_name} Contacts"
