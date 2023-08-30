
#####################
# defined functions #
#####################

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