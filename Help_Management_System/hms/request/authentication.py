from django.contrib.auth.hashers import check_password, make_password
from django.core.exceptions import ObjectDoesNotExist

from request.models import User


def do_force_login(request, user):
    request.session['user_id'] = user.id
    return True


def do_login(request):
    try:
        user = User.objects.get(email=request.POST.get('email', None))
        print("do login, submitted password: " + request.POST.get('password', None))
        print("do login, submitted hashed password: " + make_password(request.POST.get('password', None)))
        print("do login, stored hashed password: " + user.password)
        if check_password(request.POST.get('password', None), user.password):
            request.session['user_id'] = user.id
            return True
        else:
            print("do login: password did not match")
            return False
    except ObjectDoesNotExist:
        print("do login: could not find user")
        return False


def do_logout(request):
    if request.session.get('user_id', None) is not None:
        # deactivate the user's session
        del request.session['user_id']


def check_logged_in(request):
    try:
        # see if user exists
        User.objects.get(id=request.session.get('user_id', None))

        # see if user has an active session
        user_id = request.session.get('user_id', None)
        return user_id is not None

    except ObjectDoesNotExist:
        return False
