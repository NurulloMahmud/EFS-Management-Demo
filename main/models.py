from itertools import groupby
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model



User = get_user_model()


class Department(models.Model):
    """
        management = 1 | maintenance = 2 | accounting = 3
    """
    name = models.CharField(max_length=20)

    def __str__(self) -> str:
        return self.name

class UserDepartment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return str(self.user.get_username()) + ' -> ' + str(self.department.name)


class Message(models.Model):
    message = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.msg + ' -> ' + str(self.user)


class Efs(models.Model):
    code = models.CharField(max_length=20)
    reference = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=15, default='available')
    date = models.DateTimeField()

    def __str__(self) -> str:
        return self.code + ' -> ' + str(self.amount)


class Used(models.Model):
    efs = models.ForeignKey(Efs, on_delete=models.CASCADE)
    given_amount = models.DecimalField(max_digits=20, decimal_places=2)  # changed to charfield to avoid type issue
    given_by = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.TextField()
    expense = models.TextField()
    fee = models.BooleanField(default=False)
    date = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if not self.given_amount:
            self.given_amount = self.efs.amount
        super().save(*args, **kwargs)


class StatusChange(models.Model):
    efs = models.ForeignKey(Efs, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    old_status = models.CharField(max_length=10)
    new_status = models.CharField(max_length=10)
    date = models.DateTimeField(default=timezone.now())

    class Meta:
        ordering = ('-date', 'efs__code')
