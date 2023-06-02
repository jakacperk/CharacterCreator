from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.urls import reverse
from django.views.generic import FormView

from character_creator.forms import CharacterCreatorForm, CharacterAttributesForm
from character_creator.models import UserCharacter, UserCharacterAttributes


class CreateCharacter(View):
    def get(self, request):
        form = CharacterCreatorForm()
        return render(request, "character_creator.html", context={'form': form})

    def post(self, request):
        form = CharacterCreatorForm(request.POST)
        if not form.is_valid():
            error_msg = 'Your character lvl must be between 1-20'
            return render(request, "character_creator.html", context={'form': form, 'error_msg': error_msg})
        if form.is_valid():
            name = form.cleaned_data['name']
            request.session['name'] = name
            level = form.cleaned_data['level']
            race = form.cleaned_data['race']
            characterClass = form.cleaned_data['characterClass']
            c = UserCharacter(name=name, level=level, race=race, characterClass=characterClass)
            c.save()
            return HttpResponseRedirect(reverse('add-attributes'))



"""class CreateCharacter(FormView):
    form_class = CharacterCreatorForm
    template_name = "character_creator.html"
    success_url = ''

    def form_valid(self, form):
        c = UserCharacter.objects.create_character(
            name=form.cleaned_data['name'],
            level=form.cleaned_data['level'],
            race=form.cleaned_data['race'],
            characterClass=form.cleaned_data['characterClass'],
        )
        if form.is_valid():
            c.save()
            return HttpResponseRedirect(reverse('home'))
"""

class AddAttributes(View):
    def get(self, request):
        form = CharacterAttributesForm()
        return render(request, 'attributes_add.html', context={'form' : form})

    def post(self, request):
        form = CharacterAttributesForm(request.POST)
        if form.is_valid():
            strength = form.cleaned_data['strength']
            dexterity = form.cleaned_data['dexterity']
            constitution = form.cleaned_data['constitution']
            intelligence = form.cleaned_data['intelligence']
            wisdom = form.cleaned_data['wisdom']
            charisma = form.cleaned_data['charisma']
            if 0 > strength > 20 or 0 > dexterity > 20 or 0 > constitution > 20 or 0 > intelligence > 20 or 0 > wisdom > 20 or 0 > charisma > 20:
                error_msg = "your ability scores must between 1-20"
                return render(request, 'attribute_add.html', context={'form': form, 'error_msg': error_msg})
            else:
                s = UserCharacterAttributes(strength=strength, dexterity=dexterity, constitution=constitution, intelligence=intelligence, wisdom=wisdom, charisma=charisma)
                s.save()
                return HttpResponseRedirect(reverse('home'))