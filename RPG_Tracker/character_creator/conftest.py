from django.contrib.auth.models import User
import pytest
from django.test import Client

from character_creator.models import UserCharacter



@pytest.fixture
def user():
    user = User.objects.create_user(username="user", password="", id=1)
    return user




@pytest.fixture
def auto_login_user(db, client, create_user, test_password):
   def make_auto_login(user=None):
       if user is None:
           user = create_user()
       client.login(username=user.username, password=test_password)
       return client, user
   return make_auto_login


@pytest.fixture
def client():
    c = Client()
    return c


@pytest.fixture
def userCharacter():
    user_id = User.objects.create(id=1)
    d = UserCharacter.objects.create(characterId=1, name="kacper", level=10, race=2,
                              characterClass=1, creatorId=user_id, hitPoints=5,
                              armourClass=10, spellSlots=1, speed=5, notes="brak",
                              background="szarlatan")
