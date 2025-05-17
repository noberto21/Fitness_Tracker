from django.db import models
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Exercise(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    muscle_group = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Workout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.user.username}'s workout on {self.date}"

class WorkoutExercise(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    sets = models.PositiveIntegerField()
    reps = models.PositiveIntegerField()
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)  # For cardio
    
    def __str__(self):
        return f"{self.exercise.name} in {self.workout}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    height = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # in cm
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # in kg
    birth_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f"Profile for {self.user.username}"

# Create your models here.
