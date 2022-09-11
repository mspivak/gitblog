from django import forms


class NewBlogForm(forms.Form):
    name = forms.CharField(label='Name', max_length=62,
                           widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Blog Name'})
    )