from django.db import models
from accounts.models import CustomUser


class Project(models.Model):
    # ----- Choices -----
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

    PRIORITY_HIGH = "High"
    PRIORITY_MEDIUM = "Medium"
    PRIORITY_LOW = "Low"

    PRIORITY_CHOICES = [
        (PRIORITY_HIGH, "High"),
        (PRIORITY_MEDIUM, "Medium"),
        (PRIORITY_LOW, "Low"),
    ]

    # ----- Core Fields -----
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    # Dates
    assigned_date = models.DateField(help_text="Date project was assigned.")
    delivery_date = models.DateField(help_text="Expected delivery date.")

    # Optional link to live project
    live_link = models.URLField(blank=True, null=True, help_text="Add the live project URL if available")

    # Ownership & assignment
    owner = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="owned_projects",
        help_text="User who created/owns this project"
    )
    assigned_to = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_projects",
        help_text="Team member assigned to this project"
    )

    # Status / Priority / Progress
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default=PRIORITY_MEDIUM)
    completion = models.PositiveIntegerField(default=0, help_text="Completion percent (0-100)")
    progress_color = models.CharField(max_length=50, default="#26c6da", help_text="CSS color used for progress bar")

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # ----- Meta -----
    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Project"
        verbose_name_plural = "Projects"

    # ----- Methods -----
    def __str__(self) -> str:
        return self.name

    def is_completed(self) -> bool:
        """Return True if project is marked as Completed or completion == 100."""
        return self.status == self.STATUS_COMPLETED or (isinstance(self.completion, int) and self.completion >= 100)

    def get_progress_color(self) -> str:
        """Return a color hex depending on completion percentage. Prefer explicit progress_color if set."""
        if self.progress_color and self.progress_color != "#26c6da":
            return self.progress_color
        if self.completion < 40:
            return "#e53935"  # red
        if self.completion < 70:
            return "#fbc02d"  # yellow
        return "#43a047"  # green


class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="project_images/")
    uploaded_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.project.name} uploaded by {self.uploaded_by}"

