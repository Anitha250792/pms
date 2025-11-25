from django import forms
from .models import DesignUpload

class DesignUploadForm(forms.ModelForm):
    class Meta:
        model = DesignUpload
        fields = ["project_name", "design_link", "assigned_to", "notes"]
        widgets = {
            "project_name": forms.TextInput(attrs={
                "class": "form-control", "placeholder": "Enter project name"
            }),
            "design_link": forms.URLInput(attrs={
                "class": "form-control", "placeholder": "Paste Figma / XD / Image link"
            }),
            "assigned_to": forms.Select(attrs={
                "class": "form-select"
            }),
            "notes": forms.Textarea(attrs={
                "class": "form-control", "rows": 3, "placeholder": "Add design notes (optional)"
            }),
        }
