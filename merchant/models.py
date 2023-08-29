##################
# django imports #
##################
from django.db import models


##########################################
#    import modules from another app     #
##########################################
from accounts.models import CustomUser, UserProfile

#####################
# create class here #
#####################
class Merchant(models.Model):

    #####################
    #  defined fields   #
    #####################
    user = models.OneToOneField(CustomUser, related_name='customuser', on_delete=models.CASCADE)
    user_profile = models.OneToOneField(UserProfile, related_name='userprofile', on_delete=models.CASCADE)
    merchant_name = models.CharField(max_length=50)

    # vendor_slug = models.SlugField(max_length=100, unique=True)
    merchant_license = models.ImageField(upload_to='merchant/license', null=True)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


    #####################
    # defined functions #
    #####################
    def __str__(self):
        return self.merchant_name