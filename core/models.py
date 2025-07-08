from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    email=models.EmailField(max_length=100, unique=True)

    def __str__(self):
        return self.username
    


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Basic Info
    full_name = models.CharField(max_length=100)
    university = models.CharField(max_length=100)
    field_of_study = models.CharField(max_length=100)
    academic_year = models.CharField(
        max_length=20,
        choices=[
            ('Freshman', 'Freshman'),
            ('Sophomore', 'Sophomore'),
            ('Junior', 'Junior'),
            ('Senior', 'Senior'),
            ('Graduate', 'Graduate'),
        ],
    )
    date_of_birth = models.DateField(null=True, blank=True)

    # Productivity Settings
    daily_goal_hours = models.DecimalField(max_digits=4, decimal_places=2, default=2.00)  # e.g., 2.5 hrs/day
    reminder_time = models.TimeField(null=True, blank=True)
    preferred_study_time = models.CharField(
        max_length=20,
        choices=[
            ('Morning', 'Morning'),
            ('Afternoon', 'Afternoon'),
            ('Evening', 'Evening'),
            ('Night', 'Night'),
        ],
        blank=True
    )

    # Visuals
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True)

    # Tracking
    is_verified = models.BooleanField(default=False)
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s profile"
class Log(models.Model):
    user= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date=models.DateTimeField(auto_now_add=True)
    description=models.TextField()

    def __str__(self):
        return f"{self.user.username} - {self.date. strftime('%Y-%m-%d %H:%M:%S')}"
    class Meta:
        ordering = ['-date']  # Most recent logs first
    


class Todo(models.Model):
    STATUS_CHOICES= [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    task = models.CharField(max_length=255)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    due_date = models.DateField()

    def __str__(self):
        return f"{self.task} (Due: {self.due_date}, Status: {self.status})"

    class Meta:
        ordering = ['due_date']



