##################
# django imports #
##################
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

##########################################
#  import modules from current directory #
##########################################
from . models import CustomUser, UserProfile



#####################
# defined functions #
#####################


"""
In summary, this code uses signals to perform certain actions before and after saving instances of the CustomUser model. 
The post_save signal creates or updates a related UserProfile instance, while the pre_save signal prints a message when a user is being saved.
"""
# This part of the code listens for the post_save signal when a CustomUser instance is saved.
@receiver(post_save, sender=CustomUser)
def post_save_create_profile_receiver(sender, instance, created, **kwargs):

    # If a new user is created, it makes sure there's a related UserProfile instance for that user.
    if created:
        UserProfile.objects.create(user=instance)
    else:
        # If the user already exists, it tries to update their associated profile
        try:
            profile = UserProfile.objects.get(user=instance)
            profile.save()

        # If the profile doesn't exist, it creates one.
        except UserProfile.DoesNotExist:
            UserProfile.objects.create(user=instance)


"""
The purpose of this function is to print a message indicating that a user is being saved 
just before the user instance is actually saved to the database.
"""
@receiver(pre_save, sender=CustomUser)    
def pre_save_profile_receiver(sender, instance, **kwargs, ):

    # Gets the 'username' from class 'CustomUser'
    print(instance.username, 'This user is being saved')
