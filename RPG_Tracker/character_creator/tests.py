from django.test import Client
import pytest
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from character_creator.models import UserCharacter, UserCharacterAttributes, GameSession
from django.urls import reverse



@pytest.mark.django_db
def test_user_create():
  User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
  assert User.objects.count() == 1


@pytest.mark.django_db
def test_view(client):
   url = reverse('home')
   response = client.get(url)
   assert response.status_code == 200


def test_view_requires_login():
    client = Client()
    response = client.get('/characters/4/')  # jakiś widok wymagający zalogowania
    assert response.status_code == 302  # redirect
    assert response.url == '/accounts/login/?next=/characters/4/'  # na jaki adres


@pytest.mark.django_db
def test_character_addition():
    client = Client()
    response = client.get('/create_character/')
    assert response.status_code == 200
    user_character_count = UserCharacter.objects.count()
    response = client.post('/create_character/', {"name": "Dupa", "background": "1999", "characterClass":2})  # przysłane dane z formularza
    assert response.status_code == 200
    assert UserCharacter.objects.count() == user_character_count


@pytest.mark.django_db
def test_character_attributes_back(userCharacter):
    client = Client()
    response = client.get('/create_character/2/')
    assert response.status_code == 200
    user_character_count = UserCharacterAttributes.objects.count()
    response = client.post('/create_character/2', {"strenght": 1, "dexterity":1, "constitution":1, "intelligence": 1, "wisdom": 1, "charisma": 1})
    assert response.status_code == 301
    assert UserCharacterAttributes.objects.count() == user_character_count


@pytest.mark.django_db
def test_crate_session_form():
    client=Client()
    response = client.get('/session/create')
    assert response.status_code == 200
    session_count = GameSession.objects.count()
    response.client.post('/session/create', {"sessionMaster": client, "playerOneCharacter": 1, "playerTwoCharacter": 2, "playerThreeCharacter": 3, "playerFourCharacter": 4})
    assert response.status_code == 301
    assert GameSession.objects.count() == session_count



