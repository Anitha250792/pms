from django.db import models
from accounts.models import CustomUser
from django.utils.timezone import now

class DesignUpload(models.Model):
    designer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="designs_uploaded")
    assigned_to = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="designs_received")
    project_name = models.CharField(max_length=200)
    design_link = models.URLField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.project_name} → {self.assigned_to.username}"
