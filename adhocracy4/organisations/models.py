from django.db import models

class Organisation(models.Model):

    class Meta:
        swappable = 'A4_ORGANISATIONS_MODEL'
