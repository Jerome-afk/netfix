from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate
from .models import Customer, Company, FIELD_CHOICES


class UserRegisterForm(UserCreationForm):
    """
    Form for user registration
    """
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class CustomerRegisterForm(forms.ModelForm):
    """
    Form for customer-specific registration information
    """
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text='Enter your date of birth'
    )

    class Meta:
        model = Customer
        fields = ['date_of_birth']


class CompanyRegisterForm(forms.ModelForm):
    """
    Form for company-specific registration information
    """
    field_of_work = forms.ChoiceField(
        choices=FIELD_CHOICES,
        help_text='Select your field of work'
    )

    class Meta:
        model = Company
        fields = ['field_of_work']


class UserLoginForm(AuthenticationForm):
    """
    Custom login form that uses email instead of username
    """
    username = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={'autofocus': True})
    )

    def clean(self):
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if email and password:
            # Find the user by email
            try:
                user = User.objects.get(email=email)
                # Set the username field to the user's actual username
                self.cleaned_data['username'] = user.username
            except User.DoesNotExist:
                raise forms.ValidationError("Invalid email or password.")

            # Now authenticate with the username and password
            self.user_cache = authenticate(
                self.request, username=user.username, password=password
            )
            if self.user_cache is None:
                raise forms.ValidationError("Invalid email or password.")
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data
