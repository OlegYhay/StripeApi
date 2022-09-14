"""stripes URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.conf.global_settings import MEDIA_URL, MEDIA_ROOT, STATIC_ROOT
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from apiV1.views import ItemsListApiView
from stripes import settings
from stripes.settings import STATIC_URL

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', include('apiV1.urls')),
                  path('cart/', include('cart.urls')),
                  path('', include('items.urls')),
                  path('', ItemsListApiView.as_view(), name='home'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
