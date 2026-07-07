from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Household Management
    path('households/', views.household_list, name='household_list'),
    path('households/add/', views.add_household, name='add_household'),
    path('households/<int:household_id>/edit-budget/', views.edit_budget, name='edit_budget'),
    
    # Members & Details
    path('households/<int:household_id>/', views.household_detail, name='household_detail'),
    path('households/<int:household_id>/add-member/', views.add_member, name='add_member'),
    path('households/<int:household_id>/remove-member/<int:member_id>/', views.remove_member, name='remove_member'),
]
