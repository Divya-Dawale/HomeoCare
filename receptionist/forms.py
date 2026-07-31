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

    phone = forms.CharField(
    max_length=10,
    widget=forms.TextInput(
        attrs={
            "maxlength": "10",
            "pattern": "[6-9][0-9]{9}",
            "placeholder": "9876543210",
            "oninput": "this.value=this.value.replace(/[^0-9]/g,'')"
        }
    )
)

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