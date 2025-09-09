
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('homeapp.urls')),
    path('user/',include('users.urls')),
    path('option/',include('CRUD.urls')),
    path('accounts/', include('allauth.urls')),
    path("__reload__/",include("django_browser_reload.urls")),
]
