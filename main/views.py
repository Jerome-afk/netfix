from django.shortcuts import render
from services.models import Service


def home(request):
    """
    Home page view that shows recent services and a welcome message
    """
    recent_services = Service.objects.all().order_by('-created_at')[:5]
    context = {
        'recent_services': recent_services,
        'title': 'Home'
    }
    return render(request, 'main/home.html', context)


def logout_page(request):
    """
    Logout confirmation page
    """
    return render(request, 'main/logout.html', {'title': 'Logged Out'})
