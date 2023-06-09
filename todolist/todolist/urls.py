"""todolist URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path, include
from drf_spectacular.views import SpectacularSwaggerView, SpectacularAPIView

from .settings import DEBUG


urlpatterns = [
        path('core/', include('core.urls'), name="core"),
        path("oauth/", include("social_django.urls", namespace="social")),
        path("goals/", include("goals.urls"), name="goals"),
        path("bot/", include("bot.urls"), name="bot"),
    ]
if DEBUG:
    urlpatterns += [
        path('admin/', admin.site.urls),
        path(
            "docs/",
            SpectacularSwaggerView.as_view(url_name="schema"),
            name="swagger-ui",
        ),
        path("docs/schema/", SpectacularAPIView.as_view(), name="schema"),
    ]
