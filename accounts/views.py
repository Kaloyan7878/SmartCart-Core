from django.shortcuts import render, redirect, get_object_or_404
from .models import Household, HouseholdMembership
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth.models import User

# Create your views here.
# 1. Autentication
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("household_list")
    else:
        form = UserCreationForm()
    return render(request, "accounts/register.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("household_list")
    else:
        form = AuthenticationForm()
    return render(request, "accounts/login.html", {"form": form})

def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("login")
    
# 2. Manage households
def household_list(request):
    memberships = HouseholdMembership.objects.filter(user=request.user)
    return render(request, "accounts/household_list.html", {"memberships": memberships})

def add_household(request):
    if request.method == "POST":
        name = request.POST.get("name")
        budget = request.POST.get("budget_monthly");
        household = Household.objects.create(name=name, budget_monthly=budget)
        HouseholdMembership.objects.create(
            user = request.user,
            household = household,
            role=HouseholdMembership.Role.ADMIN
        )
        return redirect("household_list")
    return render(request, "accounts/add_household.html")

def edit_budget(request, household_id):
    household = get_object_or_404(Household, pk=household_id)
    is_admin = HouseholdMembership.objects.filter(
        user=request.user, 
        household=household, 
        role=HouseholdMembership.Role.ADMIN
    ).exists()

    if not is_admin:
        return redirect("household_list")
    if request.method == "POST":
        new_budget = request.POST.get("budget_monthly")
        household.budget_monthly = new_budget
        household.save()
        return redirect("household_list")
    return render(request, "accounts/edit_budget.html", {"household": household})

# 3. Members and details
def household_detail(request, household_id):
    household = get_object_or_404(Household, pk=household_id)
    members = HouseholdMembership.objects.filter(household=household)
    return render(request, "accounts/household_detail.html", {"household": household, "members": members})

def add_member(request, household_id):
    household = get_object_or_404(Household, pk=household_id)
    if request.method == "POST":
        username_to_add = request.POST.get("username")
        try:
            user_to_add = User.objects.get(username = username_to_add)
            HouseholdMembership.objects.create(
                user=user_to_add,
                household=household,
                role=HouseholdMembership.Role.MEMBER
            )
        except User.DoesNotExist:
            return render(request, "accounts/add_member.html", {"error": "Потребителят не съществува!"})
        return redirect("household_detail", household_id=household.id)
    return render(request, "accounts/add_member.html", {"household": household})

def remove_member(request, household_id, member_id):
    household = get_object_or_404(Household, pk=household_id)
    membership = get_object_or_404(
        HouseholdMembership, 
        household=household, 
        user_id=member_id
    )
    membership.delete()
    messages.success(request, "User removed from household!")
    return redirect('household_detail', household_id=household.id)


