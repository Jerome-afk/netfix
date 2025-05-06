from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save

# Field of work choices for companies
FIELD_CHOICES = [
    ('Air Conditioner', 'Air Conditioner'),
    ('All in One', 'All in One'),
    ('Carpentry', 'Carpentry'),
    ('Electricity', 'Electricity'),
    ('Gardening', 'Gardening'),
    ('Home Machines', 'Home Machines'),
    ('Housekeeping', 'Housekeeping'),
    ('Interior Design', 'Interior Design'),
    ('Locks', 'Locks'),
    ('Painting', 'Painting'),
    ('Plumbing', 'Plumbing'),
    ('Water Heaters', 'Water Heaters'),
]


class Customer(models.Model):
    """
    Customer model that extends the User model with additional information
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer')
    date_of_birth = models.DateField()

    def __str__(self):
        return f"{self.user.username}'s Customer Profile"


class Company(models.Model):
    """
    Company model that extends the User model with additional information
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='company')
    field_of_work = models.CharField(max_length=50, choices=FIELD_CHOICES)

    def __str__(self):
        return f"{self.user.username}'s Company Profile"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Signal handler to create corresponding customer or company profile when a user is created
    """
    # This is a placeholder for the signal handler
    # The actual profile creation happens during registration
    pass
