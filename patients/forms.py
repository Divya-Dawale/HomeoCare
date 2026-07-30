from django import forms
from .models import Patient


class PatientForm(forms.ModelForm):
    GENDER_CHOICES = [

        ("Male", "Male"),
        ("Female", "Female"),
        ("Other", "Other"),

    ]

    gender = forms.ChoiceField(
        choices=GENDER_CHOICES
    )
    class Meta:

        model = Patient

        fields = [
            "full_name",
            "phone",
            "email",
            "age",
            "gender",
            "address"
        ]