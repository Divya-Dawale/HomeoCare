from django import forms
from .models import Patient

class PatientForm(forms.ModelForm):

    class Meta:
        model = Patient
        fields = [
            "full_name",
            "phone",
            "email",
            "age",
            "gender",
            "address",
        ]

        widgets = {
            "gender": forms.Select(
                choices=[
                    ("Male", "Male"),
                    ("Female", "Female"),
                    ("Other", "Other"),
                ]
            ),
        }

from django import forms
from .models import MedicalHistory


class MedicalHistoryForm(forms.ModelForm):

    BLOOD_GROUP_CHOICES = [

        ("", "Select Blood Group"),

        ("A+", "A+"),
        ("A-", "A-"),

        ("B+", "B+"),
        ("B-", "B-"),

        ("AB+", "AB+"),
        ("AB-", "AB-"),

        ("O+", "O+"),
        ("O-", "O-"),

    ]

    blood_group = forms.ChoiceField(
        choices=BLOOD_GROUP_CHOICES,
        required=False
    )

    class Meta:

        model = MedicalHistory

        fields = [

            "blood_group",

            "height",
            "weight",

            "allergies",

            "chronic_diseases",

            "previous_surgeries",

            "family_history",

            "current_medications",

            "smoking",

            "alcohol",

            "emergency_person",

            "emergency_contact",

        ]