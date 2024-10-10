from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    birth_date = forms.DateField(
        required=True,
        label="Дата рождения",
        widget=forms.DateInput(attrs={
            'placeholder': 'ДД.ММ.ГГГГ',
            'type': 'date'
        })
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'birth_date', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'Имя'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Фамилия'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'password1': forms.PasswordInput(attrs={'placeholder': 'Пароль'}),
            'password2': forms.PasswordInput(attrs={'placeholder': 'Подтверждение пароля'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.help_text = ''  # Убираем стандартные подсказки
            field.widget.attrs.update({'class': 'form-control'})  # Добавляем класс Bootstrap для стилизации
