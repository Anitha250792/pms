# design/forms.py
from django import forms
from .models import DesignUpload

class DesignUploadForm(forms.ModelForm):
    class Meta:
        model = DesignUpload
        fields = ["design_file", "design_link", "notes"]
        labels = {
            "design_file": "Upload Design File",
            "design_link": "Design Link (Optional)",
            "notes": "Comments / Notes",
        }
