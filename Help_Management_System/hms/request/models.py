from datetime import datetime

from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.db import models


class Group(models.Model):
    name = models.CharField(max_length=100, default="")

    def __str__(self):
        return self.name


class User(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=100, default="")
    password = models.CharField(max_length=100, default="")
    email = models.CharField(max_length=100, default="")
    created_on = models.DateTimeField(default=datetime.now)
    role = models.CharField(max_length=100, default="user")

    def __str__(self):
        return self.fullname

    def clean(self):
        errors = []
        if self.fullname == "":
            errors.append('Full Name is required')
        if self.password == '':
            errors.append('Password is required')
        if self.email == "":
            errors.append('Email is required')
        if len(errors) > 0:
            error_str = ", ".join(errors)
            raise ValidationError(error_str)

    def hash_password(self):
        self.password = make_password(self.password)


class Tag(models.Model):
    name = models.CharField(max_length=100, default="")

    def __str__(self):
        return self.name


class Request(models.Model):
    status = models.CharField(max_length=100, default="")
    tags = models.ManyToManyField(Tag)
    title = models.CharField(max_length=100, default="")
    request_message = models.TextField(default="")
    requester = models.ForeignKey(User, on_delete=models.CASCADE)
    created_on = models.DateTimeField(default=datetime.now)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    response_message = models.TextField(default="", blank=True)
    active = models.CharField(max_length=100, default="True")

    def clean(self):
        errors = []
        if self.title == "":
            errors.append('Title is required')
        if self.request_message == '':
            errors.append('Request Message is required')
        if self.status is None:
            errors.append('Status is required')

        if len(errors) > 0:
            error_str = ", ".join(errors)
            raise ValidationError(error_str)

    def __str__(self):
        return self.title
