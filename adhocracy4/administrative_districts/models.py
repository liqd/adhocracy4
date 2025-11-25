from django.db import models


class AdministrativeDistrict(models.Model):
    name = models.CharField(max_length=128)
    short_code = models.CharField(
        max_length=2,
        blank=True,
        verbose_name="Short code",
        help_text='2-character code for the district (e.g., "mi" for Mitte)',
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
