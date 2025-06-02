from django import forms
from .models import User, Project


class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'role', 'semester', 'department','roll_number']
    
    def clean_roll_number(self):
        roll_number = self.cleaned_data.get('roll_number')
        if User.objects.filter(roll_number=roll_number).exists():
            raise forms.ValidationError("A user with this roll number already exists.")
        return roll_number

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # never force them always; we’ll validate in clean()
        self.fields['semester'].required   = False
        self.fields['department'].required = False
        self.fields['roll_number'].required = True

    def clean(self):
        cleaned = super().clean()
        role    = cleaned.get('role')
        semester   = cleaned.get('semester')
        department = cleaned.get('department')
        roll_number = cleaned.get('roll_number')


        if role == 'Student' and not semester:
            self.add_error('semester', 'Semester is required for Students.')
        if role == 'Student' and not roll_number:
            self.add_error('roll_number', 'Roll number is required for Students.')
        if role == 'Supervisor' and not department:
            self.add_error('department', 'Department is required for Supervisors.')

        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
    

class SigninForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class ProjectSubmissionForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'srs_file', 'sdd_file', 'ui_ux_file', 'repo_link', 'project_category']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }

    def __init__(self, *args, **kwargs):
        super(ProjectSubmissionForm, self).__init__(*args, **kwargs)
        # Make these fields optional
        for field in ['repo_link', 'srs_file', 'sdd_file', 'ui_ux_file']:
            self.fields[field].required = False

    def clean_srs_document(self):
        srs = self.cleaned_data.get('srs_file')
        if srs and not srs.name.endswith(('.docx')):
            raise forms.ValidationError('Only DOCX file is allowed for SRS.')
        return srs
    
    def clean_sdd_document(self):
        sdd = self.cleaned_data.get('sdd_file')
        if sdd and not sdd.name.endswith(('.docx')):
            raise forms.ValidationError('Only PDF and DOCX file is allowed for SDD.')
        return sdd
    
    def clean_ui_ux_file(self):
        uiux = self.cleaned_data.get('ui_ux_file')
        if uiux and not uiux.name.endswith(('.pdf', '.docx')):
            raise forms.ValidationError("Only PDF or DOCX files are allowed for UI/UX.")
        return uiux


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'email', 'department', 'semester', 'roll_number', 'profile_picture',
        ]