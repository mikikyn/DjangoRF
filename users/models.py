from django.contrib.auth.models import User
from django.db import models
import random


class ConfirmCode(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, related_name='confirm_code')
    code = models.CharField(max_length=6, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def generate_code(self):
        self.code = f'{random.randint(100000, 999999)}'
        self.save()


    def __str__(self):
        return f'{self.user.username} - {self.code}'