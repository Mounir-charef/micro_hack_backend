from django.db import models
from django.core.validators import FileExtensionValidator


class File(models.Model):
    file_name = models.FileField(
        upload_to="static/files_admin",
        validators=[FileExtensionValidator(allowed_extensions=[".txt"])],
    )

    def __str__(self):
        return self.file_name.name.split("/")[1]


class SummarizerManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def create(self, **kwargs):
        return super().create(**kwargs)


class Summarizer(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.FileField(
        upload_to="static/documents/",
        verbose_name="File",
        validators=[FileExtensionValidator(allowed_extensions=["txt"])],
    )
    summary = models.TextField(
        verbose_name="Summary",
        null=True,
        blank=True,
    )

    scores = models.JSONField(
        verbose_name="Scores",
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = SummarizerManager()

    class Meta:
        db_table = "summarizer"
        verbose_name = "Summary"
        verbose_name_plural = "Summaries"

    def __str__(self):
        return self.text
