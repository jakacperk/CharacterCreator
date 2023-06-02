from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings

CLASSES = (
    (1, "barbarian"),
    (2, "bard"),
    (3, "cleric"),
    (4, "druid"),
    (5, "fighter"),
    (6, "monk"),
    (7, "paladin"),
    (8, "ranger"),
    (9, "rogue"),
    (10, "sorcerer"),
    (11, "warlock"),
    (12, "wizard"),
)

RACES = (
    (1, "dragonborn"),
    (2, "dwarf"),
    (3, "elf"),
    (4, "gnome"),
    (5, "half-elf"),
    (6, "half-orc"),
    (7, "halfling"),
    (8, "human"),
    (9, "tiefling"),
)

User = settings.AUTH_USER_MODEL


class UserCharacter(models.Model):
    characterId = models.AutoField(primary_key=True)
    creatorId = models.ForeignKey(User, default=1, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=128)
    race = models.IntegerField(choices=RACES, default=1)
    level = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(20)])
    characterClass = models.IntegerField(choices=CLASSES)

    def __str__(self):
        return f"{self.name}"


class UserCharacterAttributes(models.Model):
    strength = models.IntegerField(default=1)
    dexterity = models.IntegerField(default=1)
    constitution = models.IntegerField(default=1)
    intelligence = models.IntegerField(default=1)
    wisdom = models.IntegerField(default=1)
    charisma = models.IntegerField(default=1)
    whichCharacter = models.OneToOneField(UserCharacter, on_delete=models.CASCADE, primary_key=True)
