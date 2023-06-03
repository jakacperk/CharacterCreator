from django import forms

from character_creator.models import UserCharacter, UserCharacterAttributes

INTEGER_CHOICES = [tuple([x, x]) for x in range(1, 21)]

CLASSES = [
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
]

RACES = [
    (1, "dragonborn"),
    (2, "dwarf"),
    (3, "elf"),
    (4, "gnome"),
    (5, "half-elf"),
    (6, "half-orc"),
    (7, "halfling"),
    (8, "human"),
    (9, "tiefling"),
]

"""class CharacterCreatorForm(forms.Form):
    name = forms.CharField(max_length=128)
    level = forms.IntegerField(label="Select your characters level", widget=forms.Select(choices=INTEGER_CHOICES))
    race = forms.IntegerField(label="Select your race", widget=forms.Select(choices=RACES))
    characterClass = forms.IntegerField(label="Select your class", widget=forms.Select(choices=CLASSES))"""


class CharacterCreatorForm(forms.ModelForm):
    class Meta:
        model = UserCharacter
        exclude = ('creatorId', 'proficiencyBonus')

class CharacterAttributesForm(forms.ModelForm):
    class Meta:
        model = UserCharacterAttributes
        exclude = ('whichCharacter',)


