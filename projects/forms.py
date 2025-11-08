from django import forms
from accounts.models import CustomUser
from .models import Project, ProjectImage


class ProjectForm(forms.ModelForm):
    assigned_to = forms.ModelChoiceField(
        queryset=CustomUser.objects.filter(role="Team Member"),
        required=False,
        label="Assign To (Team Member)",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Project
        fields = [
            'name', 'description', 'assigned_date', 'delivery_date',
            'assigned_to', 'status', 'priority', 'live_link'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'assigned_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'delivery_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'live_link': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://example.com (optional)'
            }),
        }


# ✅ Custom widget subclass that actually allows multiple image uploads
class MultiFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class ProjectImageForm(forms.ModelForm):
    image = forms.ImageField(
        label="Upload Project Images",
        widget=MultiFileInput(attrs={'class': 'form-control', 'multiple': True})  # 👈 Notice this
    )

    class Meta:
        model = ProjectImage
        fields = ['image']
