from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .models import Workout, WorkoutExercise, Exercise, UserProfile
from .forms import WorkoutForm, WorkoutExerciseForm, UserForm, UserProfileForm

@login_required
def dashboard(request):
    workouts = Workout.objects.filter(user=request.user).order_by('-date')[:5]
    total_workouts = Workout.objects.filter(user=request.user).count()
    total_exercises = WorkoutExercise.objects.filter(workout__user=request.user).count()
    last_workout = Workout.objects.filter(user=request.user).order_by('-date').first()
    
    return render(request, 'fitness/dashboard.html', {
        'workouts': workouts,
        'total_workouts': total_workouts,
        'total_exercises': total_exercises,
        'last_workout_date': last_workout.date if last_workout else None
    })

@login_required
def create_workout(request):
    if request.method == 'POST':
        form = WorkoutForm(request.POST)
        if form.is_valid():
            workout = form.save(commit=False)
            workout.user = request.user
            workout.save()
            return redirect('fitness:add_exercise', workout_id=workout.id)
    else:
        form = WorkoutForm()
    return render(request, 'fitness/create_workout.html', {'form': form})

@login_required
def add_exercise(request, workout_id):
    workout = get_object_or_404(Workout, id=workout_id, user=request.user)
    if request.method == 'POST':
        form = WorkoutExerciseForm(request.POST)
        if form.is_valid():
            exercise = form.save(commit=False)
            exercise.workout = workout
            exercise.save()
            return redirect('fitness:add_exercise', workout_id=workout.id)
    else:
        form = WorkoutExerciseForm()
    exercises = WorkoutExercise.objects.filter(workout=workout)
    return render(request, 'fitness/add_exercise.html', {
        'form': form,
        'workout': workout,
        'exercises': exercises
    })

@login_required
def view_workout(request, workout_id):
    workout = get_object_or_404(Workout, id=workout_id, user=request.user)
    exercises = WorkoutExercise.objects.filter(workout=workout)
    return render(request, 'fitness/view_workout.html', {
        'workout': workout,
        'exercises': exercises
    })

@login_required
def profile(request):
    user = request.user
    try:
        profile = user.userprofile
    except UserProfile.DoesNotExist:
        profile = UserProfile(user=user)
        profile.save()
    
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('fitness:profile')
    else:
        user_form = UserForm(instance=user)
        profile_form = UserProfileForm(instance=profile)
    
    return render(request, 'fitness/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('fitness:dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})