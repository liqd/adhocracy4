from django.db import models

class Organisation(models.Model):

    class Meta:
        swappable = 'A4_ORGANISATIONS_MODEL'


    def has_initiator(self, user):
        return user.is_staff
