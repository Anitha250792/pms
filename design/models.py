# design/models.py
from django.db import models
from accounts.models import CustomUser
from projects.models import Project

class DesignUpload(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="design_uploads")
    uploaded_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="uploaded_designs")
    
    version = models.PositiveIntegerField(default=1)

    design_file = models.FileField(upload_to="designs/", blank=True, null=True)
    design_link = models.URLField(blank=True, null=True)

    notes = models.TextField(blank=True, null=True)

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.project.name} - v{self.version}"
