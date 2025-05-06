from django.db import models
from django.utils import timezone
from users.models import Company, Customer, FIELD_CHOICES


# Remove 'All in One' from service field choices
SERVICE_FIELD_CHOICES = [choice for choice in FIELD_CHOICES if choice[0] != 'All in One']


class Service(models.Model):
    """
    Service model for service offerings
    """
    name = models.CharField(max_length=100)
    description = models.TextField()
    field = models.CharField(max_length=50, choices=SERVICE_FIELD_CHOICES)
    price_per_hour = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(default=timezone.now)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='services')

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-created_at']


class RequestedService(models.Model):
    """
    Model for service requests made by customers
    """
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='requests')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='requested_services')
    address = models.CharField(max_length=255)
    service_time = models.PositiveIntegerField(help_text="Service time in hours")
    calculated_cost = models.DecimalField(max_digits=10, decimal_places=2)
    requested_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.customer.user.username} requested {self.service.name}"
    
    def save(self, *args, **kwargs):
        # Calculate the cost based on service time and price per hour
        if not self.calculated_cost:
            self.calculated_cost = self.service.price_per_hour * self.service_time
        super().save(*args, **kwargs)
    
    class Meta:
        ordering = ['-requested_at']

