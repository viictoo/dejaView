import uuid
from django.db import models
from videos.models import Video
from phonenumber_field.modelfields import PhoneNumberField

STATUS = ((1, "Pending"), (0, "Complete"))

class Transaction(models.Model):
    """This model records all the mpesa payment transactions"""
    transaction_no = models.CharField(
        default=uuid.uuid4, max_length=50, unique=True)
    phone_number = PhoneNumberField(null=False, blank=False)
    checkout_request_id = models.CharField(max_length=200)
    reference = models.CharField(max_length=40, blank=True)
    description = models.TextField(null=True, blank=True)
    amount = models.CharField(max_length=10)
    status = models.CharField(
        max_length=15, choices=STATUS, default=1)
    receipt_no = models.CharField(
        max_length=200, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    ip = models.CharField(max_length=200, blank=True, null=True)
    video = models.ForeignKey(
        Video, on_delete=models.SET_NULL, null=True, blank=True)

    def __unicode__(self):
        return f"{self.transaction_no}"

    def __str__(self):
        return f'{self.transaction_no}'
