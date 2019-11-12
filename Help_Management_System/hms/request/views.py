from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.views.decorators.cache import cache_control

from request.models import User, Group, Request, Tag
from request.authentication import do_force_login, do_logout, do_login, check_logged_in


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def about(request):
    if check_logged_in(request):
        context = {
            'full_name': User.objects.get(id=request.session['user_id']).fullname
        }
        return render(request, "request/about.html", context)
    else:
        return redirect('access_denied')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def dashboard(request):
    # authenticate
    if not check_logged_in(request):
        return redirect('access_denied')

    # get user
    user = User.objects.get(id=request.session.get("user_id"))

    # get requests
    context = {}
    if user.role == "user":
        context = {
            'full_name': User.objects.get(id=request.session['user_id']).fullname,
            'requests': user.request_set.all(),
            'active_requests': user.request_set.filter(active="True"),
            'inactive_requests': user.request_set.filter(active="False"),
        }
    elif user.role == "admin":
        context = {
            'full_name': User.objects.get(id=request.session['user_id']).fullname,
            'requests': Request.objects.all(),
            'active_requests': Request.objects.filter(active="True"),
            'inactive_requests': Request.objects.filter(active="False"),
        }
    return render(request, "request/dashboard.html", context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def create_request(request):
    # authenticate
    if not check_logged_in(request):
        return redirect('access_denied')

    # get user
    user = User.objects.get(id=request.session.get("user_id"))

    # handle new requests
    if request.method == 'GET':
        context = {
            'group_id': user.group.name,
            'tags': [x.name for x in Tag.objects.all()],
        }
        return render(request, "request/create_request.html", context)

    if request.method == 'POST':
        try:
            new_request = Request(
                status=request.POST.get("requestStatus", None),
                title=request.POST.get("request-title", None),
                request_message=request.POST.get("request-message", None),
                requester=user,
                group=user.group,
                response_message=request.POST.get("response-message", None),
            )
            new_request.clean()
            new_request.save()
            new_tags = [Tag.objects.get(name=tag_name) for tag_name in request.POST.getlist("details-tags", None)]
            new_request.tags.set(new_tags)
            return redirect('dashboard')
        except ValidationError as error:
            context = {
                'group_id': user.group.name,
                'tags': [x.name for x in Tag.objects.all()],
                'error_message': error.message
            }
            return render(request, "request/create_request.html", context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def edit_request(request):
    # authenticate
    if not check_logged_in(request):
        return redirect('access_denied')

    # get user
    user = User.objects.get(id=request.session.get("user_id"))

    # get the existing request
    request_object = Request.objects.get(id=request.GET.get('request_id', None))

    if request.method == "GET":
        # Populate the form
        context = {
            'group_id': user.group.name,
            'tags': [x.name for x in Tag.objects.all()],
            'full_name': User.objects.get(id=request.session['user_id']).fullname,
            'request': request_object,
            'request_tags_names': [x.name for x in request_object.tags.all()]
        }
        return render(request, "request/edit_request.html", context)

    elif request.method == "POST":
        try:
            # Update all request fields
            request_object.title = request.POST.get("request-title", None)
            request_object.status = request.POST.get("requestStatus", None)
            request_object.request_message = request.POST.get("request-message", None)
            request_object.response_message = request.POST.get("response-message", None)
            new_tags = [Tag.objects.get(name=tag_name) for tag_name in request.POST.getlist("details-tags", None)]
            request_object.tags.set(new_tags)
            request_object.clean()
            request_object.save()
            return redirect('dashboard')
        except ValidationError as error:
            context = {
                'error_message': error.message,
            }
            return render(request, "request/edit_request.html", context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def delete_request(request):
    # authenticate
    if not check_logged_in(request):
        return redirect('access_denied')

    # get user
    user = User.objects.get(id=request.session.get("user_id"))

    # find the existing request
    request_object = Request.objects.get(id=request.POST.get('request_id', None))

    # delete existing request
    request_object.delete()
    return redirect('dashboard')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def activate_request(request):
    # authenticate
    if not check_logged_in(request):
        return redirect('access_denied')

    # get user
    user = User.objects.get(id=request.session.get("user_id"))

    # find the existing request
    request_object = Request.objects.get(id=request.POST.get('request_id', None))

    # activate existing request
    request_object.active = "True"
    request_object.save()
    return redirect('dashboard')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def deactivate_request(request):
    # authenticate
    if not check_logged_in(request):
        return redirect('access_denied')

    # get user
    user = User.objects.get(id=request.session.get("user_id"))

    # find the existing request
    request_object = Request.objects.get(id=request.POST.get('request_id', None))

    # deactivate existing requests
    request_object.active = "False"
    request_object.save()
    return redirect('dashboard')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logout(request):
    if check_logged_in(request):
        do_logout(request)
        return render(request, "request/logout.html")
    else:
        return redirect('access_denied')


def create_account(request):
    if request.method == 'GET':
        return render(request, "request/create_account.html")

    if request.method == 'POST':
        try:
            group_id = request.POST.get('groupID', None)
            if group_id is not None:
                group = Group.objects.get(name=group_id)
                new_user = User(
                    group=group,
                    fullname=request.POST.get('fullname', None),
                    password=request.POST.get('password', None),
                    email=request.POST.get('email', None),
                    role="user",
                )
                new_user.clean()
                new_user.hash_password()
                new_user.save()
                do_force_login(request, new_user)
                return redirect('dashboard')
        except ValidationError as error:
            context = {
                "error_message": error.message
            }
            return render(request, "request/create_account.html", context)
        except ObjectDoesNotExist:
            context = {
                "error_message": "invalid group id"
            }
            return render(request, "request/create_account.html", context)


def login(request):
    if request.method == 'GET':
        return render(request, "request/login.html")
    elif request.method == 'POST':
        if do_login(request):
            return redirect('dashboard')
        else:
            context = {
                'error_message': "Invalid credentials"
            }
            return render(request, "request/login.html", context)


def page_not_found(request):
    return render(request, "request/page_not_found.html")


def access_denied(request):
    return render(request, "request/access_denied.html")
