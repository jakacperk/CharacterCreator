# Generated by Django 4.0.2 on 2023-05-28 16:06

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserCharacter',
            fields=[
                ('characterId', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=128)),
                ('race', models.IntegerField(choices=[(1, 'dragonborn'), (2, 'dwarf'), (3, 'elf'), (4, 'gnome'), (5, 'half-elf'), (6, 'half-orc'), (7, 'halfling'), (8, 'human'), (9, 'tiefling')], default=1)),
                ('level', models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(20)])),
                ('characterClass', models.IntegerField(choices=[(1, 'barbarian'), (2, 'bard'), (3, 'cleric'), (4, 'druid'), (5, 'fighter'), (6, 'monk'), (7, 'paladin'), (8, 'ranger'), (9, 'rogue'), (10, 'sorcerer'), (11, 'warlock'), (12, 'wizard')])),
                ('creatorId', models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserCharacterAttributes',
            fields=[
                ('strength', models.IntegerField(default=1)),
                ('dexterity', models.IntegerField(default=1)),
                ('constitution', models.IntegerField(default=1)),
                ('intelligence', models.IntegerField(default=1)),
                ('wisdom', models.IntegerField(default=1)),
                ('charisma', models.IntegerField(default=1)),
                ('whichCharacter', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='character_creator.usercharacter')),
            ],
        ),
    ]