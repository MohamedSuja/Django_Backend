from django.db import models
from django.utils.translation import gettext_lazy as _

class Role(models.Model):
    name = models.CharField(_('name'), max_length=50, unique=True)
    description = models.TextField(_('description'), blank=True)
    permissions = models.JSONField(_('permissions'), default=list)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
    class Meta:
        verbose_name = _('role')
        verbose_name_plural = _('roles')
    
    def __str__(self):
        return self.name