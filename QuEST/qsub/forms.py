from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import models
from models import *
from django import forms

class PlayerCreationForm(UserCreationForm):
    
    school = forms.CharField(max_length=100)
    
    def save(self, commit=False):
        user = super(PlayerCreationForm, self).save(commit=False)
        user.save()
        
        try:
            profile = user.get_profile()
        except:
            profile = Player(user=user)
            
        profile.school = self.cleaned_data['school']
        profile.save()
        
        return user
    
class TournamentForm(forms.ModelForm):
    
    class Meta:
        model = Tournament
        exclude = ['owner', 'public', 'distribution']
    
    def __init__(self, read_only=False, *args, **kwargs):
        super(TournamentForm, self).__init__(*args, **kwargs)
        if read_only:
            for field in self.fields:
                self.fields[field].widget.attrs['readonly'] = True
                print self.fields[field].widget.attrs
        else:
            self.fields['player_to_add'] = forms.CharField(max_length=100, required=False)
            self.fields['hd_player_to_add'] = forms.IntegerField(widget=forms.HiddenInput, required=False)
            self.fields['public'] = forms.BooleanField(required=False)
        
class TeamForm(forms.ModelForm):
    
    class Meta:
        model = Team
        exclude = ('team_owner')
        
    def __init__(self, read_only=False, *args, **kwargs):
        super(TeamForm, self).__init__(*args, **kwargs)
        if read_only:
            for field in self.fields:
                self.fields[field].widget.attrs['readonly'] = True
        else:
            self.fields['teammate_to_add'] = forms.CharField(max_length=100, required=False)
            self.fields['hd_teammate_to_add'] = forms.IntegerField(widget=forms.HiddenInput, required=False)

class SchoolForm(forms.ModelForm):
    
    class Meta:
        model = School
        exclude = ('created_by')
        
    def __init__(self, read_only=False, *args, **kwargs):
        super(SchoolForm, self).__init__(*args, **kwargs)
        print 'read_only:', read_only
        if read_only:
            print 'read only'
            for field in self.fields:
                self.fields[field].widget.attrs['readonly'] = True
        else:
            pass
        

class RoleAssignmentForm(forms.ModelForm):
    
    class Meta:
        model = Role
        exclude = ['player', 'tournament']
        
    def __init__(self, categories=None, *args, **kwargs):
        super(RoleAssignmentForm, self).__init__(*args, **kwargs)
        self.fields['category'] = forms.MultipleChoiceField(widget=forms.SelectMultiple(attrs={'size': len(CATEGORIES)}), choices=CATEGORIES)
        if categories:
            self.initial['category'] = categories
    
    #editor = forms.IntegerField(widget=forms.HiddenInput, required=True)
    #tournament = forms.IntegerField(widget=forms.HiddenInput, required=True)
    #categories = forms.MultipleChoiceField(widget=forms.SelectMultiple, choices=CATEGORIES)
    #can_view_others = forms.BooleanField(required=False)
    #can_edit_others = forms.BooleanField(required=False)
    
class TeamRoleAssignmentForm(forms.ModelForm):
    
    class Meta:
        model = TeamRole
        exclude = ['team', 'player']
        
    def __init__(self, categories=None, *args, **kwargs):
        super(TeamRoleAssignmentForm, self).__init__(*args, **kwargs)
        self.fields['category'] = forms.MultipleChoiceField(widget=forms.SelectMultiple(attrs={'size': len(CATEGORIES)}), choices=CATEGORIES)
        #self.fields['can_view_others'].required = False
        #self.fields['can_edit_others'].required = False
        if categories:
            self.initial['category'] = categories
    #writer = forms.IntegerField(widget=forms.HiddenInput, required=True)
    #team = forms.IntegerField(widget=forms.HiddenInput, required=True)
    #categories = forms.MultipleChoiceField(widget=forms.SelectMultiple(attrs={'size': len(CATEGORIES)}), choices=CATEGORIES)
    #can_view_others = forms.BooleanField(required=False)
    #can_edit_others = forms.BooleanField(required=False)
    
class TossupForm(forms.ModelForm):
    
    subtype = forms.CharField(max_length=500, required=False)
    time_period = forms.CharField(max_length=500, required=False)
    location = forms.CharField(max_length=500, required=False)
    
    tossup_text = forms.CharField(widget=forms.Textarea(attrs={'class': 'question_text field span8', 'cols': 80, 'rows': 12}))
    tossup_answer = forms.CharField(widget=forms.Textarea(attrs={'class': 'question_text field span8', 'cols': 80, 'rows': 5}))
    
    class Meta:
        model = Tossup
        exclude = ['packet', 'author', 'locked']
        
class BonusForm(forms.ModelForm):
    
    subtype = forms.CharField(max_length=500, required=False)
    time_period = forms.CharField(max_length=500, required=False)
    location = forms.CharField(max_length=500, required=False)
    
    leadin = forms.CharField(widget=forms.Textarea(attrs={'class': 'question_text', 'cols': 80, 'rows': 2}))
    part1_text = forms.CharField(widget=forms.Textarea(attrs={'class': 'question_text', 'cols': 80, 'rows': 2}))
    part1_answer = forms.CharField(widget=forms.Textarea(attrs={'class': 'question_text', 'cols': 80, 'rows': 2}))
    part2_text = forms.CharField(widget=forms.Textarea(attrs={'class': 'question_text', 'cols': 80, 'rows': 2}))
    part2_answer = forms.CharField(widget=forms.Textarea(attrs={'class': 'question_text', 'cols': 80, 'rows': 2}))
    part3_text = forms.CharField(widget=forms.Textarea(attrs={'class': 'question_text', 'cols': 80, 'rows': 2}))
    part3_answer = forms.CharField(widget=forms.Textarea(attrs={'class': 'question_text', 'cols': 80, 'rows': 2}))
    
    class Meta:
        model = Bonus
        exclude = ['packet', 'author', 'locked']

class DistributionForm(forms.ModelForm):
    
    name = forms.CharField(max_length=100)
    
    class Meta:
        model = Distribution
    
class DistributionEntryForm(forms.ModelForm):
    
    entry_id = forms.IntegerField(widget=forms.HiddenInput, required=False)
    category = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'width': 100}))
    subcategory = forms.CharField(max_length=100, widget=forms.TextInput(attrs={}), required=False)
    num_tossups = forms.IntegerField(widget=forms.TextInput(attrs={'width': 20, 'class': 'spinner'}))
    num_bonuses = forms.IntegerField(widget=forms.TextInput(attrs={'width': 20, 'class': 'spinner'}))
    fin_tossups = forms.IntegerField(widget=forms.TextInput(attrs={'width': 20, 'class': 'spinner'}))
    fin_bonuses = forms.IntegerField(widget=forms.TextInput(attrs={'width': 20, 'class': 'spinner'}))
    
    delete = forms.BooleanField(widget=forms.CheckboxInput, required=False)
    
    class Meta:
        model = DistributionEntry
        exclude = ['distribution']
#    class Meta:
#        model = Distribution
#            
#    def __init__(self, instance=None):
#        super(DistributionForm, self).__init__()
            
#    def clean(self):
#        
#        cleaned_data = {}
#
#        for field in self.data:
#            if field == 'name':
#                cleaned_data[filed] = str(self.data[field])
#            else:
#                cleaned_data[field] = [str(value) for value in self.data.getlist(field)]
#                
#        return cleaned_data