##################
# django imports #
##################
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage, message
from django.conf import settings

#####################
# defined functions #
#####################

# This function is used to send a verification email to a user when they register or sign up on a website
def send_verification_email(request, user, mail_subject, email_template):
    
    # Gets the default "from" email 
    from_email = settings.DEFAULT_FROM_EMAIL 

    # Get the website's current domain (like "example.com").
    current_site = get_current_site(request)
    
    # The email's content is created using an HTML template, which includes the user's details and a verification link with unique tokens.
    message = render_to_string(email_template, {
        'user': user,
        'domain': current_site,

        # Get user Primary Key > convert the PK into bytes > encode the bytes into URL-safe string format
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),

        # function of the token generator takes a user object as an argument and generates a unique token associated with that user
        'token': default_token_generator.make_token(user),
    })
    
    to_email = user.email # receipient email address
    mail = EmailMessage(mail_subject, message, from_email, to=[to_email]) # Email object is created with the subject, content, sender, and recipient.
    mail.content_subtype = "html" # Indicates that the email content is HTML.
    mail.send()


def send_notification(mail_subject, mail_template, context):
    from_email = settings.DEFAULT_FROM_EMAIL
    message = render_to_string(mail_template, context)
    if(isinstance(context['to_email'], str)):
        to_email = []
        to_email.append(context['to_email'])
    else:
        to_email = context['to_email']
    mail = EmailMessage(mail_subject, message, from_email, to=to_email)
    mail.content_subtype = "html"
    mail.send()


# Below Function is used for detecting the user role.
def detectUser(user):
    if user.role == 1:
        redirectUrl = 'merchantDashboard'
        return redirectUrl
    elif user.role == 2:
        redirectUrl = 'customerDashboard'
        return redirectUrl
    elif user.role == None and user.is_superadmin:
        redirectUrl = '/admin'
        return redirectUrl