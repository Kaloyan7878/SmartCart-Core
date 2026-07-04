from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Household(models.Model):
    name = models.CharField(max_length=100)
    budget_monthly = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.name


class HouseholdMembership(models.Model):
    class Role(models.TextChoices):
        ADMIN = "admin", "Администратор"
        MEMBER = "member", "Член"
        VIEWER = "viewer", "Само преглед"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    household = models.ForeignKey(Household, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.MEMBER)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["user", "household"]

    def __str__(self):
        return f"{self.user.username} @ {self.household.name} ({self.role})"