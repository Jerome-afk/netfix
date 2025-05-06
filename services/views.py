from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from .models import Service, RequestedService, SERVICE_FIELD_CHOICES
from .forms import ServiceForm, ServiceRequestForm
from users.models import Customer, Company


class ServiceListView(ListView):
    """
    View for listing all services in chronological order
    """
    model = Service
    template_name = 'services/service_list.html'
    context_object_name = 'services'
    ordering = ['-created_at']
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'All Services'
        return context


class ServiceDetailView(DetailView):
    """
    View for displaying service details
    """
    model = Service
    template_name = 'services/service_detail.html'
    context_object_name = 'service'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.name
        
        # Add request form for customers
        if self.request.user.is_authenticated:
            try:
                # Check if user is a customer
                customer = self.request.user.customer
                context['request_form'] = ServiceRequestForm()
                context['is_customer'] = True
            except Customer.DoesNotExist:
                context['is_customer'] = False
        
        return context


@method_decorator(login_required, name='dispatch')
class ServiceCreateView(CreateView):
    """
    View for creating a new service (only for companies)
    """
    model = Service
    form_class = ServiceForm
    template_name = 'services/service_create.html'
    success_url = reverse_lazy('service-list')

    def get(self, request, *args, **kwargs):
        # Check if user is a company
        try:
            company = request.user.company
        except Company.DoesNotExist:
            messages.error(request, "Only companies can create services.")
            return redirect('home')
        return super().get(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Pass the company field to the form to restrict service fields
        kwargs['company'] = self.request.user.company
        return kwargs

    def form_valid(self, form):
        form.instance.company = self.request.user.company
        messages.success(self.request, f"Service '{form.instance.name}' has been created!")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Service'
        return context


class ServiceCategoryView(ListView):
    """
    View for listing services in a specific category
    """
    model = Service
    template_name = 'services/service_category.html'
    context_object_name = 'services'
    paginate_by = 9

    def get_queryset(self):
        category = self.kwargs.get('category')
        return Service.objects.filter(field=category).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.kwargs.get('category')
        context['category'] = category
        context['title'] = f'{category} Services'
        return context


class MostRequestedServicesView(ListView):
    """
    View for listing the most requested services
    """
    model = Service
    template_name = 'services/most_requested.html'
    context_object_name = 'services'
    paginate_by = 9

    def get_queryset(self):
        # Get services ordered by the number of requests
        return Service.objects.annotate(
            request_count=Count('requests')
        ).order_by('-request_count')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Most Requested Services'
        return context


@login_required
def request_service(request, pk):
    """
    View for customers to request a service
    """
    service = get_object_or_404(Service, pk=pk)
    
    # Check if user is a customer
    try:
        customer = request.user.customer
    except Customer.DoesNotExist:
        messages.error(request, "Only customers can request services.")
        return redirect('service-detail', pk=pk)
    
    if request.method == 'POST':
        form = ServiceRequestForm(request.POST)
        if form.is_valid():
            service_request = form.save(commit=False)
            service_request.service = service
            service_request.customer = customer
            service_request.calculated_cost = service.price_per_hour * service_request.service_time
            service_request.save()
            
            messages.success(request, f"You have successfully requested the service '{service.name}'.")
            return redirect('profile')
    else:
        form = ServiceRequestForm()
    
    return render(request, 'services/service_request.html', {
        'form': form,
        'service': service,
        'title': f'Request {service.name}'
    })
