from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    """Form for creating and editing tasks"""
    class Meta:
        model = Task
        fields = ['title', 'description', 'project', 'due_date', 'status', 'priority']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'project': forms.Select(attrs={'class': 'form-select'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
        }
