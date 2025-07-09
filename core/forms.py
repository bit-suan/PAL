from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Todo, Log, UserProfile  

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',
                'style': 'width: 100%; padding: 10px; margin: 5px 0; border: 1px solid #ddd; border-radius: 5px;'
            })

class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['task', 'due_date', 'status']  
        widgets = {
            'task': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your task...',
                'style': 'width: 100%; padding: 10px; margin: 5px 0; border: 1px solid #ddd; border-radius: 5px;'
            }),
            'due_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'style': 'width: 100%; padding: 10px; margin: 5px 0; border: 1px solid #ddd; border-radius: 5px;'
            }),
            'status': forms.Select(attrs={
                'class': 'form-control',
                'style': 'width: 100%; padding: 10px; margin: 5px 0; border: 1px solid #ddd; border-radius: 5px;'
            }),
        }

class LogForm(forms.ModelForm):
    class Meta:
        model = Log
        fields = ['description']  # Your Log model only has description field (date is auto-added)
        widgets = {
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'What did you work on today?',
                'rows': 4,
                'style': 'width: 100%; padding: 10px; margin: 5px 0; border: 1px solid #ddd; border-radius: 5px; resize: vertical;'
            }),
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile  
        fields = [
            'full_name', 
            'university', 
            'field_of_study', 
            'academic_year',
            'date_of_birth',
            'daily_goal_hours',
            'reminder_time',
            'preferred_study_time',
            'bio',
            'profile_picture'
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your full name',
                'style': 'width: 100%; padding: 10px; margin: 5px 0; border: 1px solid #ddd; border-radius: 5px;'
            }),
            'university': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your university',
                'style': 'width: 100%; padding: 10px; margin: 5px 0; border: 1px solid #ddd; border-radius: 5px;'
            }),
            'field_of_study': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your field of study',
                'style': 'width: 100%; padding: 10px; margin: 5px 0; border: 1px solid #ddd; border-radius: 5px;'
            }),
            'academic_year': forms.Select(attrs={
                'class': 'form-control',
                'style': 'width: 100%; padding: 10px; margin: 5px 0; border: 1px solid #ddd; border-radius: 5px;'
            }),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'style': 'width: 100%; padding: 10px; margin: 5px 0; border: 1px solid #ddd; border-radius: 5px;'
            }),
            'daily_goal_hours': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.5',
                'min': '0.5',
                'max': '24',
                'placeholder': '2.5',
                'style': 'width: 100%; padding: 10px; margin: 5px 0; border: 1px solid #ddd; border-radius: 5px;'
            }),
            'reminder_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time',
                'style': 'width: 100%; padding: 10px; margin: 5px 0; border: 1px solid #ddd; border-radius: 5px;'
            }),
            'preferred_study_time': forms.Select(attrs={
                'class': 'form-control',
                'style': 'width: 100%; padding: 10px; margin: 5px 0; border: 1px solid #ddd; border-radius: 5px;'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Tell us about yourself...',
                'rows': 4,
                'style': 'width: 100%; padding: 10px; margin: 5px 0; border: 1px solid #ddd; border-radius: 5px; resize: vertical;'
            }),
            'profile_picture': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
                'style': 'width: 100%; padding: 10px; margin: 5px 0; border: 1px solid #ddd; border-radius: 5px;'
            }),
        }

# Login form 
class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username',
            'style': 'width: 100%; padding: 10px; margin: 5px 0; border: 1px solid #ddd; border-radius: 5px;'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password',
            'style': 'width: 100%; padding: 10px; margin: 5px 0; border: 1px solid #ddd; border-radius: 5px;'
        })
    )