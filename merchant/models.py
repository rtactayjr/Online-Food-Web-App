##################
# django imports #
##################
from django.db import models
from datetime import time, date, datetime
from enum import unique

##########################################
#    import modules from another app     #
##########################################
from accounts.models import CustomUser, UserProfile
from accounts.utils import send_notification

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
    merchant_slug = models.SlugField(max_length=100, unique=True, blank=True, null=True)
    merchant_license = models.ImageField(upload_to='merchant/license', null=True)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


    #####################
    # defined functions #
    #####################
    def __str__(self):
        return self.merchant_name
    
    # Override the save method to perform additional actions
    def save(self, *args, **kwargs):

        # Check if the instance already exists in the database (not a new instance)
        if self.pk is not None:

            # Retrieve the original instance of the Merchant model before the update
            orig = Merchant.objects.get(pk=self.pk)

            # Check if the 'is_approved' field has changed between the original and updated instances
            if orig.is_approved != self.is_approved:

                mail_template = 'accounts/emails/admin_approval_email.html'
                context = {
                    'user': self.user,
                    'is_approved': self.is_approved,
                    'to_email': self.user.email,
                }

                if self.is_approved == True:

                    # Send a notification email for approval
                    mail_subject = "Congratulations! Your restaurant has been approved."
                    send_notification(mail_subject, mail_template, context)
                else:
                    # Send a notification email for disapproval
                    mail_subject = "We're sorry! You are not eligible for publishing your food menu on our marketplace."
                    send_notification(mail_subject, mail_template, context)

        # Save the updated Merchant instance and return the result 
        return super(Merchant, self).save(*args, **kwargs)