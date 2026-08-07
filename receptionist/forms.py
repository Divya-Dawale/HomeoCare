from django import forms
from accounts.models import User

class ProfileForm(forms.ModelForm):

    class Meta:

        model = User

        fields = [

            "first_name",
            "last_name",
            "username",
            "email",
            "phone"

        ]

        widgets = {

            "phone": forms.TextInput(
                attrs={
                    "maxlength": "10",
                    "pattern": "[0-9]{10}",
                    "placeholder": "Enter Phone Number"
                }
            )

        }

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

class ReceptionistProfileForm(forms.ModelForm):
    def clean_email(self):

        email = self.cleaned_data["email"]

        if User.objects.exclude(
            pk=self.instance.pk
        ).filter(
            email=email
        ).exists():

            raise forms.ValidationError(
                "This email is already in use."
            )

        return email
    def clean_username(self):

        username = self.cleaned_data["username"]

        if User.objects.exclude(
            pk=self.instance.pk
        ).filter(
            username=username
        ).exists():

            raise forms.ValidationError(
                "This username already exists."
            )

        return username

    class Meta:

        model = User

        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "phone",
        ]

        widgets = {

            "first_name": forms.TextInput(),

            "last_name": forms.TextInput(),

            "username": forms.TextInput(),

            "email": forms.EmailInput(),

            "phone": forms.TextInput(),

        }