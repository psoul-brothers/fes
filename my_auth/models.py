from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.base_user import BaseUserManager

from django.utils import timezone

class MyManager(BaseUserManager):
    def create_user(self, username, password='pass-123', **extra_fields):
        now = timezone.now()
        
        user = self.model(
                employee_number = username,
                is_active=True,
                last_login=now,
                date_joined=now,
                **extra_fields                
            )
        user.set_password(password)
        user.save(using=self._db)
        return user
        
    def create_superuser(self, username, password, **extra_fields):
        user = self.create_user(username, password)
        user.is_active = True
        user.is_staff = True
        user.is_admin = True
        # user.is_superuser = True
        user.save(using=self._db)
        return user
