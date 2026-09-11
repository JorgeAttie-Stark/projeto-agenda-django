from django.db import models
from django.utils.timezone import now


class Contact(models.Model):

    first_name = models.CharField(max_length=100)

    last_name = models.CharField(max_length=50, blank=True)

    email = models.EmailField(max_length=254)

    phone = models.CharField(max_length=100, null=True, blank=True)

    message = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(default=now)

    updated_at = models.DateTimeField(default=now)

    description = models.TextField(null=True, blank=True)

    show = models.BooleanField(default=True)

    picture = models.ImageField(blank=True, upload_to='pictures/%Y/%m/%d/')

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"
