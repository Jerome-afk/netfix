from django.urls import path
from . import views

urlpatterns = [
    path('', views.ServiceListView.as_view(), name='service-list'),
    path('<int:pk>/', views.ServiceDetailView.as_view(), name='service-detail'),
    path('create/', views.ServiceCreateView.as_view(), name='service-create'),
    path('category/<str:category>/', views.ServiceCategoryView.as_view(), name='service-category'),
    path('most-requested/', views.MostRequestedServicesView.as_view(), name='most-requested'),
    path('<int:pk>/request/', views.request_service, name='request-service'),
]
