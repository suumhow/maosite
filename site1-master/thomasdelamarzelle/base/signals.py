from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import Student


def student_profile(sender, instance, created, **kwargs):
    if created:
        Student.objects.create(
            user=instance,
            name=instance.first_name + ' ' +instance.last_name,
        )
post_save.connect(student_profile, sender=User)