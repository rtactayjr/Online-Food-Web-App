##################
# django imports #
##################
from django.apps import AppConfig


#####################
# create class here #
#####################

class AccountsConfig(AppConfig):

    #####################
    # defined Fields #
    #####################
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    #####################
    # defined functions #
    #####################
    """
    This method is called when the app is ready. It's used to perform any necessary setup or configuration. 
    In this case, it's used to import the accounts.signals module, which contains signal handlers.

    'accounts' = app, 'signals' = signals.py under accounts app.
    """
    def ready(self):
        import accounts.signals
