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
    

    def is_open(self):
        # Check current day's opening hours.
        today_date = date.today()
        today = today_date.isoweekday()
        
        current_opening_hours = OperatingHour.objects.filter(merchant=self, day=today)
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")

        is_open = None
        for i in current_opening_hours:
            if not i.is_closed:
                start = str(datetime.strptime(i.from_hour, "%I:%M %p").time())
                end = str(datetime.strptime(i.to_hour, "%I:%M %p").time())
                if current_time > start and current_time < end:
                    is_open = True
                    break
                else:
                    is_open = False
        return is_open




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
    



DAYS = [
    (1, ("Monday")),
    (2, ("Tuesday")),
    (3, ("Wednesday")),
    (4, ("Thursday")),
    (5, ("Friday")),
    (6, ("Saturday")),
    (7, ("Sunday")),
]

HOUR_OF_DAY_24 = [(time(h, m).strftime('%I:%M %p'), time(h, m).strftime('%I:%M %p')) for h in range(0, 24) for m in (0, 30)]

class OperatingHour(models.Model):
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE)
    day = models.IntegerField(choices=DAYS)
    from_hour = models.CharField(choices=HOUR_OF_DAY_24, max_length=10, blank=True)
    to_hour = models.CharField(choices=HOUR_OF_DAY_24, max_length=10, blank=True)
    is_closed = models.BooleanField(default=False)

    class Meta:
        ordering = ('day', '-from_hour')
        unique_together = ('merchant', 'day', 'from_hour', 'to_hour')

    def __str__(self):
        return self.get_day_display()