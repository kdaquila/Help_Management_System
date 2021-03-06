"""hms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from request import views

urlpatterns = [
    path('', views.login, name="login"),
    path('about/', views.about, name="about"),
    path('create_account/', views.create_account, name="create_account"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('create_request/', views.create_request, name="create_request"),
    path('edit_request/', views.edit_request, name="edit_request"),
    path('delete_request/', views.delete_request, name="delete_request"),
    path('activate_request/', views.activate_request, name="activate_request"),
    path('deactivate_request/', views.deactivate_request, name="deactivate_request"),
    path('logout/', views.logout, name="logout"),
    path('admin/', admin.site.urls),
    path('access_denied/', views.access_denied, name='access_denied'),
    re_path(r'^.*/$', views.page_not_found, name="page_not_found")
]
