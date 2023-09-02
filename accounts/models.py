##################
# django imports #
##################
from django.db import models
from django.db.models.fields.related import OneToOneField

from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


#####################
# create class here #
#####################

# This class will not contain fields just methods
# Inherit BaseUserManager
class CustomUserManager(BaseUserManager):

    #####################
    # defined functions #
    #####################

    # This function handles user creation.
    def create_user(self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError("User must provide an email address")
    
        if not username:
            raise ValueError("User must provide a username")
        
        # Passing the value to 'user'
        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
        )

        # Hashes the password using a secure algorithm (hash)
        user.set_password(password)

        # Save using the current database connection
        user.save(using=self._db)
        return user
    
    # This function handles user SuperUser creation.
    def create_superuser(self, first_name, last_name, username, email, password=None ):

        # Passing values to user
        user =  self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password,
            first_name = first_name,
            last_name = last_name,
        )

        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True

        # Save using the current database connection
        user.save(using=self._db)
        return user


# This class will allow us to define our own fields and methods.
# Inherit AbstractBaseUser
class CustomUser(AbstractBaseUser):

    # Setup custom 'Role' for user.
    MERCHANT = 1
    CUSTOMER = 2

    ROLE_CHOICE = (
        (MERCHANT, 'Merchant'),
        (CUSTOMER, 'Customer'),
    )

    #####################
    #  defined fields   #
    #####################

    # Required fields during sign up.
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)

    phone_number = models.CharField(max_length=12, blank=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICE, blank=True, null=True)

    # Required fields with assigned values
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    # Customize the behavior of user authentication and management.
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    # Replace default manager with 'CustomUserManager'
    objects = CustomUserManager()

    #####################
    # defined functions #
    #####################

    # Defined to return the email address of the user.
    def __str__(self):
        return self.email

    # Defined method simply returns whether the user is an admin.
    # perm (permission)
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # Method is used to check if a user has permissions to access a specific module (app) within the application.
    def has_module_perms(self, app_label):
        return True
    
    # Method is used to check what the user role is.
    def get_role(self):
        if self.role == 1:
            user_role = 'Merchant'
        elif self.role == 2:
            user_role = 'Customer'
        return user_role
    
# Creating Custom-UserProfile
class UserProfile(models.Model):

    #####################
    #  defined fields   #
    #####################

    # set user to 'OnetoOneFields' since one user can only have one profile
    user = OneToOneField(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='users/profile_pictures', blank=True, null=True)
    cover_photo = models.ImageField(upload_to='users/cover_photos', blank=True, null=True)
    address_line_1 = models.CharField(max_length=250, blank=True, null=True)
    address_line_2 = models.CharField(max_length=250, blank=True, null=True)
    country = models.CharField(max_length=15, blank=True, null=True)
    state = models.CharField(max_length=15, blank=True, null=True)
    city = models.CharField(max_length=15, blank=True, null=True)
    pin_code = models.CharField(max_length=6, blank=True, null=True)
    latitude = models.CharField(max_length=20, blank=True, null=True)
    longitude = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    #####################
    # defined functions #
    #####################

    # Defined to return the complete address
    def full_address(self):
        return f'{self.address_line_1}, {self.address_line_2}'

    # Defined to return the email address of the user.
    def __str__(self):
        return self.user.email
