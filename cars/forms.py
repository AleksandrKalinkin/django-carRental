from django import forms
from django.core.exceptions import ValidationError
from datetime import date


class BookingForm(forms.Form):
    first_name = forms.CharField(
        label='Имя',
        required=True,
        widget=forms.TextInput(attrs={'readonly': 'readonly', 'class': 'form-control'})
    )
    last_name = forms.CharField(
        label='Фамилия',
        required=True,
        widget=forms.TextInput(attrs={'readonly': 'readonly', 'class': 'form-control'})
    )
    phone = forms.CharField(
        label='Телефон',
        required=True,
        widget=forms.TextInput(attrs={'readonly': 'readonly', 'class': 'form-control'})
    )
    start_date = forms.DateField(
        label='Дата начала',
        widget=forms.DateInput(attrs={
            'type': 'date',
            'min': date.today().isoformat(),
            'class': 'form-control'
        })
    )
    end_date = forms.DateField(
        label='Дата окончания',
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        })
    )
    start_time = forms.TimeField(
        label='Время начала',
        widget=forms.TimeInput(attrs={
            'type': 'time',
            'class': 'form-control'
        })
    )
    end_time = forms.TimeField(
        label='Время окончания',
        widget=forms.TimeInput(attrs={
            'type': 'time',
            'class': 'form-control'
        })
    )
    child_seat = forms.BooleanField(
        label='Детское кресло (+500 ₽/сутки)',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date:
            if start_date > end_date:
                raise ValidationError('Дата окончания должна быть после даты начала')
            if (end_date - start_date).days > 30:
                raise ValidationError('Максимальный срок аренды - 30 дней')

        return cleaned_data