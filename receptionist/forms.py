from django import forms
from accounts.models import User

class ProfileForm(forms.ModelForm):

    class Meta:
        model = User

        fields = [
            "first_name",
            "last_name",
            "email",
        ]

from django import forms
from patients.models import Patient


class PatientAppointmentForm(forms.ModelForm):

    GENDER_CHOICES = [

        ("Male", "Male"),
        ("Female", "Female"),
        ("Other", "Other"),

    ]

    gender = forms.ChoiceField(
        choices=GENDER_CHOICES
    )

    appointment_date = forms.DateField(
        widget=forms.DateInput(
            attrs={"type": "date"}
        )
    )

    reason_for_visit = forms.CharField(
        widget=forms.Textarea(
            attrs={"rows": 3}
        )
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