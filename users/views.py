from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from .forms import UserRegisterForm, CustomerRegisterForm, CompanyRegisterForm, UserLoginForm
from django.contrib.auth.views import LoginView
from .models import Customer, Company
from services.models import Service, RequestedService


class CustomLoginView(LoginView):
    """
    Custom login view that uses email for authentication
    """
    template_name = 'users/login.html'
    authentication_form = UserLoginForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Login'
        return context


@transaction.atomic
def register(request):
    """
    View for user registration
    Handles both customer and company registration
    """
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        user_type = request.POST.get('user_type')
        
        if user_type == 'customer':
            profile_form = CustomerRegisterForm(request.POST)
        else:  # company
            profile_form = CompanyRegisterForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            # Check if email or username already exists
            email = user_form.cleaned_data.get('email')
            username = user_form.cleaned_data.get('username')
            
            if User.objects.filter(email=email).exists():
                messages.error(request, 'This email is already registered.')
                return render(request, 'users/register.html', {
                    'user_form': user_form,
                    'customer_form': CustomerRegisterForm(),
                    'company_form': CompanyRegisterForm(),
                    'title': 'Register'
                })
            
            if User.objects.filter(username=username).exists():
                messages.error(request, 'This username is already taken.')
                return render(request, 'users/register.html', {
                    'user_form': user_form,
                    'customer_form': CustomerRegisterForm(),
                    'company_form': CompanyRegisterForm(),
                    'title': 'Register'
                })
                
            # Save user and profile
            user = user_form.save()
            
            if user_type == 'customer':
                Customer.objects.create(
                    user=user,
                    date_of_birth=profile_form.cleaned_data.get('date_of_birth')
                )
                messages.success(request, 'Customer account created! You can now log in.')
            else:  # company
                Company.objects.create(
                    user=user,
                    field_of_work=profile_form.cleaned_data.get('field_of_work')
                )
                messages.success(request, 'Company account created! You can now log in.')
                
            return redirect('login')
    else:
        user_form = UserRegisterForm()
        customer_form = CustomerRegisterForm()
        company_form = CompanyRegisterForm()

    return render(request, 'users/register.html', {
        'user_form': user_form,
        'customer_form': customer_form,
        'company_form': company_form,
        'title': 'Register'
    })


@login_required
def profile(request):
    """
    View for user profile
    Shows different information based on user type (customer or company)
    """
    user = request.user
    
    # Check if the user is a customer or company
    try:
        customer = user.customer
        requested_services = RequestedService.objects.filter(customer=customer).order_by('-requested_at')
        return render(request, 'users/profile.html', {
            'user': user,
            'profile': customer,
            'requested_services': requested_services,
            'is_customer': True,
            'title': 'Profile'
        })
    except Customer.DoesNotExist:
        try:
            company = user.company
            services = Service.objects.filter(company=company).order_by('-created_at')
            return render(request, 'users/profile.html', {
                'user': user,
                'profile': company,
                'services': services,
                'is_company': True,
                'title': 'Profile'
            })
        except Company.DoesNotExist:
            messages.error(request, 'User profile not found.')
            return redirect('home')
