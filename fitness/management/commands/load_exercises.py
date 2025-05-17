from django.core.management.base import BaseCommand
from fitness.models import Exercise

class Command(BaseCommand):
    help = 'Loads initial exercise data into the database'

    def handle(self, *args, **options):
        exercises = [
            {"name": "Bench Press", "description": "Barbell chest press", "muscle_group": "Chest"},
            {"name": "Squat", "description": "Barbell squat", "muscle_group": "Legs"},
            {"name": "Deadlift", "description": "Barbell deadlift", "muscle_group": "Back"},
            {"name": "Overhead Press", "description": "Barbell shoulder press", "muscle_group": "Shoulders"},
            {"name": "Pull-up", "description": "Bodyweight pull-up", "muscle_group": "Back"},
            {"name": "Push-up", "description": "Bodyweight push-up", "muscle_group": "Chest"},
            {"name": "Bicep Curl", "description": "Dumbbell bicep curl", "muscle_group": "Arms"},
            {"name": "Tricep Dip", "description": "Bodyweight tricep dip", "muscle_group": "Arms"},
            {"name": "Running", "description": "Cardiovascular running", "muscle_group": "Cardio"},
            {"name": "Cycling", "description": "Cardiovascular cycling", "muscle_group": "Cardio"},
        ]

        for exercise_data in exercises:
            exercise, created = Exercise.objects.get_or_create(
                name=exercise_data['name'],
                defaults={
                    'description': exercise_data['description'],
                    'muscle_group': exercise_data['muscle_group']
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created exercise: {exercise.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Exercise already exists: {exercise.name}'))

        self.stdout.write(self.style.SUCCESS('Successfully loaded all exercises'))