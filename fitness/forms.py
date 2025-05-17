from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Workout, WorkoutExercise, UserProfile, Exercise
from django.utils import timezone

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email'
        })
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Choose a username'
        })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Create a password'
        })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm password'
        })
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already in use.")
        return email

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        })
    )

class WorkoutForm(forms.ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'max': timezone.now().date()
        })
    )
    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Workout notes...'
        })
    )

    class Meta:
        model = Workout
        fields = ['date', 'notes']

class WorkoutExerciseForm(forms.ModelForm):
    exercise = forms.ModelChoiceField(
        queryset=Exercise.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    sets = forms.IntegerField(
        min_value=1,
        max_value=20,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Number of sets'
        })
    )
    reps = forms.IntegerField(
        min_value=1,
        max_value=100,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Reps per set'
        })
    )
    weight = forms.DecimalField(
        required=False,
        min_value=0,
        max_value=500,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Weight (kg)',
            'step': '0.1'
        })
    )
    duration = forms.DurationField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Duration (HH:MM:SS)'
        })
    )

    class Meta:
        model = WorkoutExercise
        fields = ['exercise', 'sets', 'reps', 'weight', 'duration']

    def clean(self):
        cleaned_data = super().clean()
        weight = cleaned_data.get('weight')
        duration = cleaned_data.get('duration')

        if not weight and not duration:
            raise forms.ValidationError("Please provide either weight or duration for the exercise.")
        return cleaned_data

class UserForm(forms.ModelForm):
    first_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )
    last_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control'
        })
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class UserProfileForm(forms.ModelForm):
    height = forms.DecimalField(
        required=False,
        min_value=50,
        max_value=250,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Height in cm',
            'step': '0.1'
        })
    )
    weight = forms.DecimalField(
        required=False,
        min_value=20,
        max_value=300,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Weight in kg',
            'step': '0.1'
        })
    )
    birth_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'max': timezone.now().date()
        })
    )

    class Meta:
        model = UserProfile
        fields = ['height', 'weight', 'birth_date']

class ExerciseForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Exercise name'
        })
    )
    description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Exercise description...'
        })
    )
    muscle_group = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Primary muscle group'
        })
    )

    class Meta:
        model = Exercise
        fields = ['name', 'description', 'muscle_group']