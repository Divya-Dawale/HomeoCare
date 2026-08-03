from django import forms
from .models import MedicalHistory, MedicalRecord
FOOD_CRAVINGS_CHOICES = [
    ("Sweets", "Sweets"),
    ("Salt", "Salt"),
    ("Spicy", "Spicy"),
    ("Sour", "Sour"),
    ("Milk", "Milk"),
    ("Eggs", "Eggs"),
    ("Cold Drinks", "Cold Drinks"),
]

FEARS_CHOICES = [
    ("Darkness", "Darkness"),
    ("Heights", "Heights"),
    ("Thunderstorms", "Thunderstorms"),
    ("Crowds", "Crowds"),
    ("Animals", "Animals"),
    ("Death", "Death"),
]

TEMPERAMENT_CHOICES = [
    ("Mild", "Mild"),
    ("Irritable", "Irritable"),
    ("Anxious", "Anxious"),
    ("Fastidious", "Fastidious"),
    ("Timid", "Timid"),
    ("Jealous", "Jealous"),
    ("Suspicious", "Suspicious"),
]
class MedicalHistoryForm(forms.ModelForm):
    food_cravings = forms.MultipleChoiceField(
    choices=FOOD_CRAVINGS_CHOICES,
    widget=forms.CheckboxSelectMultiple,
    required=False
    )

    fears = forms.MultipleChoiceField(
        choices=FEARS_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    temperament = forms.MultipleChoiceField(
        choices=TEMPERAMENT_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    class Meta:

        model = MedicalHistory

        fields = [

                # Physical Metrics
                "height",
                "weight",
                "blood_group",
                "blood_pressure",
                "physical_build",
                "side_affinity",
                "thermal_state",

                # Chief Complaint
                "current_problem",
                "location_extension",
                "concomitants",
                "etiology",
                "etiology_notes",

                # Existing Fields
                "allergies",
                "past_diseases",
                "family_history",

                # Diet & Lifestyle
                "diet_type",
                "meal_pattern",
                "appetite_scale",
                "thirst_pattern",
                "food_cravings",
                "sleep_posture",

                # Psychology
                "social_disposition",
                "temperament",
                "fears",
                "pace_of_actions",
                "orderliness",
                "self_perception",
                "criticism_response",
                "ambition",
                "future_outlook",
                "anger_reaction",
                "consolation_reaction",
                "weeping_tendency",

                # Existing
                "additional_notes",

            ]

        widgets = {

            "current_problem":
                forms.Textarea(attrs={"rows": 3}),

            "location_extension":
                forms.Textarea(attrs={"rows": 2}),

            "concomitants":
                forms.Textarea(attrs={"rows": 2}),

            "etiology_notes":
                forms.Textarea(attrs={"rows": 2}),

            "allergies":
                forms.Textarea(attrs={"rows": 2}),

            "past_diseases":
                forms.Textarea(attrs={"rows": 2}),

            "family_history":
                forms.Textarea(attrs={"rows": 2}),

            "additional_notes":
                forms.Textarea(attrs={"rows": 3}),
        }
    def clean_food_cravings(self):
        return self.cleaned_data.get("food_cravings", [])

    def clean_fears(self):
        return self.cleaned_data.get("fears", [])

    def clean_temperament(self):
        return self.cleaned_data.get("temperament", [])

class MedicalRecordForm(forms.ModelForm):
    
    class Meta:

        model = MedicalRecord

        fields = [

            "symptoms",

            "observations",

            "diagnosis_notes",

            "follow_up_notes",

        ]

        widgets = {

            "symptoms": forms.Textarea(attrs={"rows":4}),

            "observations": forms.Textarea(attrs={"rows":4}),

            "diagnosis_notes": forms.Textarea(attrs={"rows":4}),

            "follow_up_notes": forms.Textarea(attrs={"rows":4}),

        }
from django import forms
from .models import DoctorSettings

from django import forms
from .models import DoctorSettings

from django import forms
from .models import DoctorSettings


class DoctorSettingsForm(forms.ModelForm):

    class Meta:

        model = DoctorSettings

        fields = [

            "consultation_fee",

            "medicine_fee_7_days",

            "max_patients_per_day",

            "phone",

            "email",

            "address",

            "opening_time",

            "closing_time",

            "google_map_link",

        ]


        widgets = {


            "phone": forms.TextInput(

                attrs={

                    "maxlength": "10",

                    "pattern": "[0-9]{10}",

                    "placeholder": "Clinic Phone Number"

                }

            ),



            "email": forms.EmailInput(

                attrs={

                    "placeholder": "Clinic Email Address"

                }

            ),



            "address": forms.Textarea(

                attrs={

                    "rows": 3,

                    "placeholder": "Clinic Address"

                }

            ),



            "opening_time": forms.TimeInput(

                attrs={

                    "type": "time"

                }

            ),



            "closing_time": forms.TimeInput(

                attrs={

                    "type": "time"

                }

            ),



            "google_map_link": forms.URLInput(

                attrs={

                    "placeholder": "Google Maps Link"

                }

            ),



            "consultation_fee": forms.NumberInput(

                attrs={

                    "placeholder": "Consultation Fee"

                }

            ),



            "medicine_fee_7_days": forms.NumberInput(

                attrs={

                    "placeholder": "Medicine Fee (7 Days)"

                }

            ),



            "max_patients_per_day": forms.NumberInput(

                attrs={

                    "placeholder": "Maximum Patients Per Day"

                }

            ),

        }
from django import forms
from accounts.models import User

class DoctorProfileForm(forms.ModelForm):

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