#from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import User

class UserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('email',)


class UserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('email',)

class SearchForm(forms.Form):
    bacterial_name = forms.CharField(max_length=100, required=False)
    nucleic_or_peptidic = forms.ChoiceField(choices = ((True,'Nucleic'),(False,'Peptidic')), required=False)
    sequence = forms.CharField(max_length = 100, min_length=3, required=False)
    gene_name = forms.CharField(max_length = 100, required=False)
    transcript_name = forms.CharField(max_length = 100, required=False)
    description = forms.CharField(max_length = 100, required=False)