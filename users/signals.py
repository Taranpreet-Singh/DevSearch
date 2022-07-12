from django.db.models.signals import post_delete, post_save
from django.contrib.auth.models import User
from .models import Profile

from django.core.mail import send_mail
from django.conf import settings


# @receiver(post_save, sender=Profile)
# connecting or creating a profile whenever a user is created
def createProfile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user = user,
            username = user.username,
            email = user.email,
            name = user.first_name,
        )
        # Everytime a new user is created we send a welcome mail
        # It will give an error if we didnt give permission to less secure apps in our google account
        subject = 'Welcome to Devsearch'
        message = 'We are glad you are here with us! '
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [profile.email],
            fail_silently=False
        )



def updateUser(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user
    if created == False:
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()


def deleteProfile(sender, instance, **kwargs):
    try:
        user = instance.user   # userof that profile, instance is of Profile
        user.delete()
    except:
        pass

post_save.connect(createProfile, sender=User) 
post_save.connect(updateUser, sender=Profile)
post_delete.connect(deleteProfile, sender=Profile)

# post_delete.connect(profileDeleted, sender=Profile)