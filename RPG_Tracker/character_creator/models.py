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
    characterId = models.AutoField(primary_key=True, unique=True)
    creatorId = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=128)
    background = models.CharField(max_length=128, default="")
    race = models.IntegerField(choices=RACES, default=1)
    level = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(20)])
    characterClass = models.IntegerField(choices=CLASSES)
    proficiencyBonus = models.CharField(max_length=2, blank=True)

    def calculate_proficiency(self):
        if self.level < 4:
            return 2
        elif 3 < self.level < 9:
            return 3
        elif 8 < self.level < 13:
            return 4
        elif 12 < self.level < 17:
            return 5
        elif 16 < self.level:
            return 6

    def save(self, *args, **kwargs):
        self.proficiencyBonus = self.calculate_proficiency()
        super(UserCharacter, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"


class UserCharacterAttributes(models.Model):
    strength = models.IntegerField(default=1)
    dexterity = models.IntegerField(default=1)
    constitution = models.IntegerField(default=1)
    intelligence = models.IntegerField(default=1)
    wisdom = models.IntegerField(default=1)
    charisma = models.IntegerField(default=1)

    acrobatics = models.IntegerField(default=0)
    acrobatics_proficient = models.BooleanField(default=False)
    animal_handling = models.IntegerField(default=0)
    animal_handling_proficient = models.BooleanField(default=False)
    arcana = models.IntegerField(default=0)
    arcana_proficient = models.BooleanField(default=False)
    athletics = models.IntegerField(default=0)
    athletics_proficient = models.BooleanField(default=False)
    deception = models.IntegerField(default=0)
    deception_proficient = models.BooleanField(default=False)
    history = models.IntegerField(default=0)
    history_proficient = models.BooleanField(default=False)
    insight = models.IntegerField(default=0)
    insight_proficient = models.BooleanField(default=False)
    intimidation = models.IntegerField(default=0)
    intimidation_proficient = models.BooleanField(default=False)
    investigation = models.IntegerField(default=0)
    investigation_proficient = models.BooleanField(default=False)
    medicine = models.IntegerField(default=0)
    medicine_proficient = models.BooleanField(default=False)
    nature = models.IntegerField(default=0)
    nature_proficient = models.BooleanField(default=False)
    perception = models.IntegerField(default=0)
    perception_proficient = models.BooleanField(default=False)
    performance = models.IntegerField(default=0)
    performance_proficient = models.BooleanField(default=False)
    persuasion = models.IntegerField(default=0)
    persuasion_proficient = models.BooleanField(default=False)
    religion = models.IntegerField(default=0)
    religion_proficient = models.BooleanField(default=False)
    sleight_of_hand = models.IntegerField(default=0)
    sleight_of_hand_proficient = models.BooleanField(default=False)
    stealth = models.IntegerField(default=0)
    stealth_proficient = models.BooleanField(default=False)
    survival = models.IntegerField(default=0)
    survival_proficient = models.BooleanField(default=False)

    def strength_bonus(self):
        return (self.strength - 10) // 2

    def dexterity_bonus(self):
        return (self.dexterity - 10) // 2

    def constitution_bonus(self):
        return (self.constitution - 10) // 2

    def intelligence_bonus(self):
        return (self.intelligence - 10) // 2

    def wisdom_bonus(self):
        return (self.wisdom - 10) // 2

    def charisma_bonus(self):
        return (self.charisma - 10) // 2

    whichCharacter = models.OneToOneField(UserCharacter, on_delete=models.CASCADE, primary_key=True)


"""class CharacterProficiences(models.Model):

    acrobatics = models.IntegerField(default=UserCharacterAttributes.dexterity)    animal_handling = models.IntegerField(default=wisdom_modifier)
    arcana = models.IntegerField(default=intelligence_modifier)
    athletics = models.IntegerField(default=strength_modifier)
    deception = models.IntegerField(default=charisma_modifier)
    history = models.IntegerField(default=intelligence_modifier)
    insight = models.IntegerField(default=wisdom_modifier)
    intimidation = models.IntegerField(default=charisma_modifier)
    investigation = models.IntegerField(default=intelligence_modifier)
    medicine = models.IntegerField(default=wisdom_modifier)
    nature = models.IntegerField(default=intelligence_modifier)
    perception = models.IntegerField(default=wisdom_modifier)
    performance = models.IntegerField(default=charisma_modifier)
    persuasion = models.IntegerField(default=charisma_modifier)
    religion = models.IntegerField(default=intelligence_modifier)
    sleight_of_hand = models.IntegerField(default=dexterity_modifier)
    stealth = models.IntegerField(default=dexterity_modifier)
    survival = models.IntegerField(default=wisdom_modifier)

    whichCharacter = models.OneToOneField(UserCharacter, on_delete=models.CASCADE, primary_key=True)"""
