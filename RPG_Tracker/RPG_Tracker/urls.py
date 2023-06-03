"""
URL configuration for RPG_Tracker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.views.generic.base import TemplateView

from character_creator.views import CreateCharacter, AddAttributes, TestView, YourCharacters, CharacterView


urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('create_character/', CreateCharacter.as_view(), name='character-creator'),
    path('create_character/2/', AddAttributes.as_view(), name='add-attributes'),
    path('test/', TestView.as_view(), name='test'),
    path('characters/', YourCharacters.as_view(), name='characters'),
    path('characters/<int:characterId>/', CharacterView.as_view(), name='character-view'),
]
