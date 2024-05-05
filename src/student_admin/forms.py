from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import StudentUser, AdminUser
from plans.plan_manage import PlanManagement
from datetime import date

# class PlanSelectionForm(forms.Form):
#     PLAN_CHOICES = [
#         ('A', 'Plan A'),
#         ('B', 'Plan B'),
#         ('C', 'Plan C'),
#     ]
#     selected_plan = forms.ChoiceField(choices=PLAN_CHOICES, widget=forms.Select(attrs={"class": "plan-select"}), initial='A')

class PlanSelectionForm(forms.Form):

    PLAN_CHOICES = [
        ('A', 'Plan A (Primary Plan)'),
        ('B', 'Plan B'),
        ('C', 'Plan C'),
    ]

    #SEMESTER_CHOICES = []
    #for year in range(cohort_year, cohort_year + 4):
        #SEMESTER_CHOICES.append((f"Fall {year}", f"Fall {year}"))
        #SEMESTER_CHOICES.append((f"Spring {year}", f"Spring {year}"))

    selected_plan = forms.ChoiceField(choices=PLAN_CHOICES, required=False, label = "",
                                      widget=forms.Select(attrs={"class": "form-control", "id": "plan"}),
                                      # Use form-control for Bootstrap styling
                                      )

    selected_sem = forms.ChoiceField(choices=[], required=False, label = "",
                                     widget=forms.Select(attrs={"class": "form-control", "id": "sem"}),
                                     # Use form-control for Bootstrap styling
                                     )


    def set_student(self, student):
        """Set the student instance separately after form initialization."""
        self.student = student
        self.update_semester_choices()

    def update_semester_choices(self):
        """Update semester choices based on the student instance."""
        if self.student:
            cohort_year = self.student.cohort-4  # Assume `cohort_year` is an attribute of the student
            SEMESTER_CHOICES = []
            for year in range(cohort_year, cohort_year + 4):
                SEMESTER_CHOICES.append((f"Fall {year}", f"Fall {year}"))
                if year < cohort_year + 4:  # Ensure it's not the last year
                    next_year = year+1
                    SEMESTER_CHOICES.append((f"Spring {next_year}", f"Spring {next_year}"))

            self.fields['selected_sem'].choices = SEMESTER_CHOICES

    #current_year = date.today().year

    #selected_plan = forms.ChoiceField(
      #  choices=PLAN_CHOICES,
      #  label="Choose Plan",
       # required=True,
    #)

        # Define the semester field with choices
    #selected_sem = forms.ChoiceField(
        #choices=semester_choices,
        #label="Semester",
       # required=True,
    #)



#Code for if we want to make extra form for year, split up year/semester
"""
    SEMESTER_CHOICES = [
        ('Fall', 'Fall'),
        ('Spring', 'Spring')
    ]

    YEAR_CHOICES = [
        ('2021', '2021'),
        ('2022', '2022'),
        ('2023', '2023'),
        ('2024', '2024'),
        ('2025', '2025')
    ]

    selected_sem = forms.ChoiceField(choices=SEMESTER_CHOICES, required = False, widget=forms.Select(attrs={"class": "form-control"}),  # Use form-control for Bootstrap styling
    )

    selected_year = forms.ChoiceField(choices=YEAR_CHOICES, required = False, widget=forms.Select(attrs={"class": "form-control"}),  # Use form-control for Bootstrap styling
    )
"""

# form to choose which semester you want to add your courses to 




class StudentForm(forms.ModelForm):
    plan_management = PlanManagement()
    MAJOR_CHOICES = [
        ('Computer Science B.A.', 'Computer Science B.A.'),
        ('Computer Science B.S.', 'Computer Science B.S.'),
        ('Mathematics B.A.', 'Mathematics B.A.'),
        # Add more choices as needed
    ]
    MAJOR_II_CHOICES = [
        ('Computer Science B.A.', 'Computer Science B.A.'),
        ('Computer Science B.S.', 'Computer Science B.S.'),
        ('Mathematics B.A.', 'Mathematics B.A.'),
        ('', 'N/A'),
        # Add more choices as needed
    ]
    MINOR_CHOICES = [
        ('Computer Science', 'Computer Science'),
        ('Mathematics', 'Mathematics'),
        ('', 'N/A'),
        # Add more choices as needed
    ]
    MINOR_II_CHOICES = [
        ('Computer Science', 'Computer Science'),
        ('Mathematics', 'Mathematics'),
        ('', 'N/A'),
        # Add more choices as needed
    ]

    COHORT_CHOICES = [
        (plan_management.senior_cohort, 'Senior'),
        (plan_management.junior_cohort, 'Junior'),
        (plan_management.sophomore_cohort, 'Sophomore'),
        (plan_management.freshmen_cohort, 'Freshmen'),
    ]

    major = forms.ChoiceField(choices=MAJOR_CHOICES, required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    major_ii = forms.ChoiceField(choices=MAJOR_II_CHOICES, required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    minor = forms.ChoiceField(choices=MINOR_CHOICES, required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    minor_ii = forms.ChoiceField(choices=MINOR_II_CHOICES, required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    cohort = forms.ChoiceField(choices=COHORT_CHOICES, required=False, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = StudentUser
        fields = [
            'major',
            'major_ii',
            'minor',
            'minor_ii',
            'cohort'
        ]
      
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['major'].label = ""
    #     self.fields["major"].widget.attrs.update({
    #         'required': False,
    #         'name': 'major',
    #         'id': 'major',
    #         'type': 'text',
    #         'class': 'form-input',
    #         'placeholder': 'Major I',
    #     })
        
    #     self.fields['major_ii'].label = ""
    #     self.fields["major_ii"].widget.attrs.update({
    #         'required': False,
    #         'name': 'major2',
    #         'id': 'major2',
    #         'type': 'text',
    #         'class': 'form-input',
    #         'placeholder': 'Major II'

    #     })

    #     self.fields['minor'].label = ""
    #     self.fields["minor"].widget.attrs.update({
    #         'required': False,
    #         'name': 'minor',
    #         'id': 'minor',
    #         'type': 'text',
    #         'class': 'form-input',
    #         'placeholder': 'Minor I'
    #     })

    #     self.fields['minor_ii'].label = ""        
    #     self.fields["minor_ii"].widget.attrs.update({
    #         'required': False,
    #         'name': 'minor2',
    #         'id': 'minor2',
    #         'type': 'text',
    #         'class': 'form-input',
    #         'placeholder': 'Minor II'
    #     })

class AdminForm(forms.ModelForm):
    class Meta:
        model = AdminUser
        fields = [
            'department'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['department'].label = ""
        self.fields["department"].widget.attrs.update({
            'required': False,
            'name': 'department',
            'id': 'department',
            'type': 'text',
            'class': 'form-input',
            'placeholder': 'Department',
        })


class ProfileForm(forms.ModelForm):
    class Meta:
        model = StudentUser
        fields = [
            'major',
            'major_ii',
            'minor',
            'minor_ii', 
            'first_name',
            'last_name',
        ]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['major'].label = ""
        self.fields["major"].widget.attrs.update({
            'required': False,
            'name': 'major',
            'id': 'major',
            'type': 'text',
            'class': 'form-input',


        })

        self.fields['major_ii'].label = ""
        self.fields["major_ii"].widget.attrs.update({
            'required': False,
            'name': 'major_ii',
            'id': 'major_ii',
            'type': 'text',
            'class': 'form-input',

        })

        self.fields['minor'].label = ""
        self.fields["minor"].widget.attrs.update({
            'required': False,
            'name': 'minor',
            'id': 'minor',
            'type': 'text',
            'class': 'form-input',

        })
        
        self.fields['minor_ii'].label = ""
        self.fields["minor_ii"].widget.attrs.update({
            'required': False,
            'name': 'minor_ii',
            'id': 'minor_ii',
            'type': 'text',
            'class': 'form-input',


        })

        self.fields['first_name'].label = ""
        self.fields["first_name"].widget.attrs.update({
            'required': False,
            'name': 'first_name',
            'id': 'first_name',
            'type': 'text',
            'class': 'form-input',

        })

        self.fields['last_name'].label = ""
        self.fields["last_name"].widget.attrs.update({
            'required': False,
            'name': 'last_name',
            'id': 'last_name',
            'type': 'text',
            'class': 'form-input',
        })

# for admin view counts
class YearSemesterForm(forms.Form):
    # Get the current year
    current_year = date.today().year

    # Create a list of choices for the year field (current year + next 3 years)
    year_choices = [(year, str(year)) for year in range(current_year, current_year + 4)]

    # Create a list of choices for the semester field (fall or spring)
    semester_choices = [
        ('fall', 'Fall'),
        ('spring', 'Spring'),
    ]

    # Define the year field with choices
    year = forms.ChoiceField(
        choices=year_choices,
        label="Year",
        required=True,
    )

    # Define the semester field with choices
    semester = forms.ChoiceField(
        choices=semester_choices,
        label="Semester",
        required=True,
    )