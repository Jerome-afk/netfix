from django import forms
from .models import Service, RequestedService, SERVICE_FIELD_CHOICES
from users.models import Company


class ServiceForm(forms.ModelForm):
    """
    Form for creating a new service
    """
    class Meta:
        model = Service
        fields = ['name', 'description', 'field', 'price_per_hour']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'price_per_hour': forms.NumberInput(attrs={'min': 0, 'step': 0.01}),
        }
    
    def __init__(self, *args, **kwargs):
        # Get the company from kwargs
        company = kwargs.pop('company', None)
        super().__init__(*args, **kwargs)
        
        # Restrict field choices based on company's field of work
        if company:
            if company.field_of_work == 'All in One':
                # All in One companies can create any type of service
                self.fields['field'].choices = SERVICE_FIELD_CHOICES
            else:
                # Other companies can only create services in their field
                self.fields['field'].choices = [(company.field_of_work, company.field_of_work)]
                self.fields['field'].initial = company.field_of_work
                self.fields['field'].widget.attrs['readonly'] = True


class ServiceRequestForm(forms.ModelForm):
    """
    Form for requesting a service
    """
    class Meta:
        model = RequestedService
        fields = ['address', 'service_time']
        widgets = {
            'address': forms.TextInput(attrs={'placeholder': 'Enter the service address'}),
            'service_time': forms.NumberInput(attrs={'min': 1, 'max': 24, 'step': 1}),
        }

