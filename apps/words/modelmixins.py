from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


class OwnerMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              verbose_name=_('Owner'),
                              on_delete=models.CASCADE)

    class Meta:
        abstract = True

    def is_owner(self, user):
        return self.owner == user or user.is_superuser
