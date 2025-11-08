from django.contrib.postgres.fields import ArrayField
from django.db import models
from accounts.models import CustomUser


class Project(models.Model):

    # ----- Status Choices -----
    STATUS_PENDING = "Pending"
    STATUS_IN_PROGRESS = "In Progress"
    STATUS_COMPLETED = "Completed"
    STATUS_ON_HOLD = "On Hold"

    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_IN_PROGRESS, "In Progress"),
        (STATUS_COMPLETED, "Completed"),
        (STATUS_ON_HOLD, "On Hold"),
    ]

    # ----- Priority Choices -----
    PRIORITY_HIGH = "High"
    PRIORITY_MEDIUM = "Medium"
    PRIORITY_LOW = "Low"

    PRIORITY_CHOICES = [
        (PRIORITY_HIGH, "High"),
        (PRIORITY_MEDIUM, "Medium"),
        (PRIORITY_LOW, "Low"),
    ]

    # ----- Main Fields -----
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    assigned_date = models.DateField(null=True, blank=True)
    delivery_date = models.DateField(null=True, blank=True)

    # Live Link
    live_link = models.URLField(blank=True, null=True)

    # Owner / Assigned To
    owner = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="owned_projects"
    )

    assigned_to = models.ManyToManyField(
    CustomUser,
    blank=True,
    related_name="assigned_projects"
)


    # Status / Priority / Progress
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING
    )

    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default=PRIORITY_MEDIUM
    )

    completion = models.PositiveIntegerField(default=0)
    progress_color = models.CharField(max_length=50, default="#26c6da")

    # ⭐ NEW: Remarks Field (Team Member can update, Manager/HR read-only)
    remark = models.TextField(blank=True, null=True)

    # ----- Timestamp Fields -----
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # ----- Meta -----
    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Project"
        verbose_name_plural = "Projects"

    # ----- Helper Methods -----
    def __str__(self):
        return self.name

    def is_completed(self):
        return (
            self.status == self.STATUS_COMPLETED
            or (isinstance(self.completion, int) and self.completion >= 100)
        )

    def get_progress_color(self):
        # If manually assigned color → use it
        if self.progress_color and self.progress_color != "#26c6da":
            return self.progress_color

        # Automatic color based on completion %
        if self.completion < 40:
            return "#e53935"  # Red
        if self.completion < 70:
            return "#fbc02d"  # Yellow
        return "#43a047"      # Green
    
    design_links = models.JSONField(default=list, blank=True)   # List of uploaded links
    design_history = models.JSONField(default=list, blank=True) # Stores full history (who uploaded, link, timestamp)


class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="project_images/")
    uploaded_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.project.name} uploaded by {self.uploaded_by}"
