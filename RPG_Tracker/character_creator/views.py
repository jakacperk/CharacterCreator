from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
import requests
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View, generic
from django.urls import reverse
from django.views.generic import FormView

from character_creator.forms import CharacterCreatorForm, CharacterAttributesForm, CreateSessionForm, SessionStatsForm
from character_creator.models import UserCharacter, UserCharacterAttributes, GameSession


class CreateCharacter(View):  # Character creator view
    def get(self, request):  # GET method
        form = CharacterCreatorForm()
        return render(request, "character_creator.html", context={'form': form})

    def post(self, request):  # POST method
        form = CharacterCreatorForm(request.POST)
        if not form.is_valid():
            error_msg = 'Your character lvl must be between 1-20'
            return render(request, "character_creator.html", context={'form': form, 'error_msg': error_msg})
        if form.is_valid():
            name = form.cleaned_data['name']
            level = form.cleaned_data['level']
            race = form.cleaned_data['race']
            characterClass = form.cleaned_data['characterClass']
            hitPoints = form.cleaned_data['hitPoints']
            armourClass = form.cleaned_data['armourClass']
            spellSlots = form.cleaned_data['spellSlots']
            speed = form.cleaned_data['speed']
            notes = form.cleaned_data['notes']
            c = UserCharacter(name=name, level=level, race=race, characterClass=characterClass, creatorId=request.user,
                              hitPoints=hitPoints, armourClass=armourClass, spellSlots=spellSlots, speed=speed,
                              notes=notes)
            c.save()
            request.session['whichCharacter'] = c.characterId
            return HttpResponseRedirect(reverse('add-attributes'))


class AddAttributes(View):  # Adding attributes to previously created characters
    def get(self, request):
        form = CharacterAttributesForm()
        return render(request, 'attributes_add.html', context={'form': form})

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
                whichCharacter = UserCharacter.objects.get(pk=request.session['whichCharacter'])
                s = UserCharacterAttributes(strength=strength, dexterity=dexterity, constitution=constitution,
                                            intelligence=intelligence, wisdom=wisdom, charisma=charisma,
                                            whichCharacter=whichCharacter)
                s.save()
                return HttpResponseRedirect(reverse('home'))



class YourCharacters(generic.ListView):  # view that lists all characters created by user
    model = UserCharacter

    def get_queryset(self):
        return UserCharacter.objects.filter(creatorId=self.request.user)


def get_context_data(self, **kwargs):
    context = super(YourCharacters, self).get_context.data(**kwargs)
    context['usercharacter'] = UserCharacter


class CharacterView(View):  # detailed view of a user character

    @method_decorator(login_required, name='dispatch')
    def get(self, request, characterId):
        userCharacter = get_object_or_404(UserCharacter, characterId=characterId)
        userCharacterAttributes = UserCharacterAttributes.objects.get(pk=userCharacter)
        return render(
            request,
            'character_data.html',
            context={
                "usercharacter": userCharacter,
                "usercharacterattributes": userCharacterAttributes
            }
        )


class EditCharacterView(View):  # View that allows editing user characters
    def get(self, request, characterId):
        userCharacter = get_object_or_404(UserCharacter, characterId=characterId)
        userCharacterAttributes = UserCharacterAttributes.objects.get(pk=userCharacter)
        character_creator_form = CharacterCreatorForm(instance=userCharacter)
        character_attributes_form = CharacterAttributesForm(instance=userCharacterAttributes)
        return render(request,
                      'edit_character.html',
                      context={'usercharacter': userCharacter,
                               'usercharacterattributes': userCharacterAttributes,
                               'character_creator_form': character_creator_form,
                               'character_attributes_form': character_attributes_form, })

    def post(self, request, characterId):
        userCharacter = get_object_or_404(UserCharacter, characterId=characterId)
        userCharacterAttributes = UserCharacterAttributes.objects.get(pk=userCharacter)
        character_creator_form = CharacterCreatorForm(request.POST, instance=userCharacter)
        character_attributes_form = CharacterAttributesForm(request.POST, instance=userCharacterAttributes)
        if not character_creator_form.is_valid():
            error_msg = 'Your character lvl must be between 1-20'
            return render(request, "character_creator.html",
                          context={'character_creator_form': character_creator_form, 'error_msg': error_msg,
                                   'character_attributes_form': character_attributes_form})
        if character_creator_form.is_valid() and character_attributes_form.is_valid():
            name = character_creator_form.cleaned_data['name']
            level = character_creator_form.cleaned_data['level']
            race = character_creator_form.cleaned_data['race']
            characterClass = character_creator_form.cleaned_data['characterClass']
            background = character_creator_form.cleaned_data['background']
            hitPoints = character_creator_form.cleaned_data['hitPoints']
            armourClass = character_creator_form.cleaned_data['armourClass']
            spellSlots = character_creator_form.cleaned_data['spellSlots']
            speed = character_creator_form.cleaned_data['speed']
            notes = character_creator_form.cleaned_data['notes']
            strength = character_attributes_form.cleaned_data['strength']
            dexterity = character_attributes_form.cleaned_data['dexterity']
            constitution = character_attributes_form.cleaned_data['constitution']
            intelligence = character_attributes_form.cleaned_data['intelligence']
            wisdom = character_attributes_form.cleaned_data['wisdom']
            charisma = character_attributes_form.cleaned_data['charisma']
            c = UserCharacter(characterId=userCharacter.characterId, name=name, level=level, race=race,
                              characterClass=characterClass, creatorId=request.user, hitPoints=hitPoints,
                              armourClass=armourClass, spellSlots=spellSlots, speed=speed, notes=notes,
                              background=background)
            c.save()
            s = UserCharacterAttributes(strength=strength, dexterity=dexterity, constitution=constitution,
                                        intelligence=intelligence, wisdom=wisdom, charisma=charisma,
                                        whichCharacter=userCharacter)
            s.save()
            return HttpResponseRedirect(reverse('characters'))


class SessionCreateView(View):  # View for creating game session
    def get(self, request):
        form = CreateSessionForm()
        return render(request, 'create_session.html', context={'form': form})

    def post(self, request):
        form = CreateSessionForm(request.POST)
        if form.is_valid():
            playerOneCharacter = form.cleaned_data['playerOneCharacter']
            playerTwoCharacter = form.cleaned_data['playerTwoCharacter']
            playerThreeCharacter = form.cleaned_data['playerThreeCharacter']
            playerFourCharacter = form.cleaned_data['playerFourCharacter']
            sesh = GameSession(sessionMaster=request.user, playerOneCharacter=playerOneCharacter,
                               playerTwoCharacter=playerTwoCharacter, playerThreeCharacter=playerThreeCharacter,
                               playerFourCharacter=playerFourCharacter)
            sesh.save()
            request.session['seshId'] = sesh.sessionId
            return HttpResponseRedirect(f'http://127.0.0.1:8000/session/view/{sesh.sessionId}')


class SessionView(View):  # View that shows current game session and deletes it when it's done
    def get(self, request, sessionId):
        sessionsStats = SessionStatsForm()
        gamesession = get_object_or_404(GameSession, sessionId=request.session['seshId'])
        playerOneAtt = UserCharacterAttributes.objects.get(pk=gamesession.playerOneCharacter)
        playerTwoAtt = UserCharacterAttributes.objects.get(pk=gamesession.playerTwoCharacter)
        playerThreeAtt = UserCharacterAttributes.objects.get(pk=gamesession.playerThreeCharacter)
        playerFourAtt = UserCharacterAttributes.objects.get(pk=gamesession.playerFourCharacter)
        return render(request, 'session_view.html', context={
            'gamesession': gamesession,
            'playerOneAtt': playerOneAtt,
            'playerTwoAtt': playerTwoAtt,
            'playerThreeAtt': playerThreeAtt,
            'playerFourAtt': playerFourAtt,
            'sessionStats': sessionsStats
        })

    def post(self, request, sessionId):
        query = GameSession.objects.get(pk=request.session['seshId'])
        query.delete()
        return HttpResponseRedirect(reverse('home'))
