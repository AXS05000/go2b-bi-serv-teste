from django import forms
from django.contrib.auth.forms import (AuthenticationForm, UserChangeForm,
                                       UserCreationForm)

from .models import CustomUsuario


class CustomUsuarioCreateForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Insira seu primeiro nome'}))
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Insira seu sobrenome'}))
    fone = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Insira seu telefone'}))
    email = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Insira seu E-mail'}))
    password1 = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Insira sua senha'}))
    password2 = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Confirme sua senha'}))

    class Meta:
        model = CustomUsuario
        fields = ('email', 'username', 'first_name',
                  'last_name', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUsuario.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "Este endereço de e-mail já está registrado. Tente outro.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if CustomUsuario.objects.filter(username=username).exists():
            raise forms.ValidationError(
                "Este nome de usuário já está em uso. Tente outro.")
        return username

    def save(self, commit=True):
        user = super(CustomUsuarioCreateForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user


class CustomUsuarioChangeForm(UserChangeForm):
    class Meta:
        model = CustomUsuario
        fields = ('first_name', 'last_name', 'fone')


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Email', 'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Senha', 'class': 'form-control'}))
