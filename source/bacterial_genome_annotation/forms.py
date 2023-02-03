# from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, ReadOnlyPasswordHashField
from django import forms
from .models import User


class UserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('email',)


class UserChangeForm(UserChangeForm):
    password = ReadOnlyPasswordHashField(label=("Password"), widget=forms.HiddenInput(),
                                         help_text=("Raw passwords are not stored, so there is no way to see "
                                                    "this user's password, but you can change the password "
                                                    "using <a href=\"../password/\">this form</a>."))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'phone_no', 'picture',)


class UserSearchForm(forms.Form):
    email = forms.CharField(max_length=100, required=False)
    first_name = forms.CharField(max_length=100, required=False)
    last_name = forms.CharField(max_length=100, required=False)
    phone_number = forms.CharField(max_length=10, required=False)
    show_only_favorites = forms.BooleanField(required=False)


class SearchForm(forms.Form):
    bacterial_name = forms.CharField(max_length=100, required=False)
    sequence = forms.CharField(max_length=100, min_length=3, required=False)
    gene_name = forms.CharField(max_length=100, required=False)
    transcript_name = forms.CharField(max_length=100, required=False)
    description = forms.CharField(max_length=100, required=False)
    nucleic_or_peptidic = forms.ChoiceField(
        choices=((True, 'Nucleic'), (False, 'Peptidic')),
        required=False
    )


class AnnotFormById(forms.Form):
    # The same than the sequence but with '.X' with X a number to allow multipple annotation.
    id = forms.CharField(max_length=50, required=False)
    gene = forms.CharField(max_length=10, required=False)
    gene_biotype = forms.CharField(max_length=50, required=False)
    transcript_biotype = forms.CharField(max_length=50, required=False)
    gene_symbol = forms.CharField(max_length=10, required=False)
    description = forms.CharField(max_length=200, required=False)
    transcript = forms.CharField(max_length=200, required=False)
    isValidate = forms.BooleanField(required=False)


class AnnotationFormBySearch(forms.Form):
    gene = forms.CharField(max_length=10, required=False)
    gene_biotype = forms.CharField(max_length=50, required=False)
    transcript_biotype = forms.CharField(max_length=50, required=False)
    gene_symbol = forms.CharField(max_length=10, required=False)
    description = forms.CharField(max_length=200, required=False)
    transcript = forms.CharField(max_length=200, required=False)


class CommentForm(forms.Form):
    comment = forms.CharField(max_length=500)


class ContactForm(forms.Form):
    name = forms.CharField(max_length=255)
    email = forms.EmailField()
    content = forms.CharField(widget=forms.Textarea)

# default=''
