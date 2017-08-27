from django import forms


class SearchForm(forms.Form):
    query = forms.CharField(required=False, label='Search Query', max_length=200)
