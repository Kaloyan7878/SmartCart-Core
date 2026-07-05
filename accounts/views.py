from django.shortcuts import render

# Create your views here.
def household_list(request):
    memberships = HouseholdMembership.objects.filter(user=request.user)
    return render(request, "accounts/household_list.html", {"memberships": memberships})

def add_household(request):
    if request.method == 


def edit_budget