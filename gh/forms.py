from django import forms


class NewBlogForm(forms.Form):
    name = forms.CharField(label='Name', max_length=62)