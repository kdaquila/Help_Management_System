from django.contrib import admin

from request.models import User, Group, Tag, Request


class RequestInline(admin.TabularInline):
    model = Request
    extra = 1


class UserAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    inlines = [RequestInline]


admin.site.register(User, UserAdmin)
admin.site.register(Group)
admin.site.register(Tag)
admin.site.register(Request)
